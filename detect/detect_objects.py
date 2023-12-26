import os
import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
from object_detection.utils import config_util
from animal_detection.data.preparation import get_label_map_path
from animal_detection.common.helpers import detection_scores_to_percentages

from animal_detection.models.train import PipelineConfigLoader
tf.config.run_functions_eagerly(True)


import argparse
import os
import glob

from animal_detection.common.config import TFOD_API_INSTALL_DIRECTORY
from animal_detection.common.cmd import CmdArgumentExtractor
from animal_detection.constants.general import MODE_DEFAULT, MODE_VERBOSE, MODE_SILENT
from animal_detection.constants.cmd import *
from animal_detection.common import config
import cv2
import numpy as np
from matplotlib import pyplot as plt
import re


LIGHT_BATCH_SIZE = 4
EXTREME_BATCH_SIZE = 8  # please only use on a performant pc


class DetectArgumentExtractor(CmdArgumentExtractor):
    # num_train_steps

    @staticmethod
    def get_parser():
        description = \
            'Script which prepares the raw dataset from perception for training'
        parser = argparse.ArgumentParser(
            description=description
        )
        full_arg_mode = CMD_ARGS[CMD_ARG_IMG_PATH][CMD_ARG_OPT_FULL]
        short_arg_mode = CMD_ARGS[CMD_ARG_IMG_PATH][CMD_ARG_OPT_SHORT]
        parser.add_argument(
            short_arg_mode, full_arg_mode,
            nargs='?', type=str
        )
        
        full_arg_mode = CMD_ARGS[CMD_ARG_CKPT][CMD_ARG_OPT_FULL]
        short_arg_mode = CMD_ARGS[CMD_ARG_CKPT][CMD_ARG_OPT_SHORT]
        parser.add_argument(
            short_arg_mode, full_arg_mode,
            nargs='?', type=str
        )
        
        full_arg_mode = CMD_ARGS[CMD_ARG_DETECTION_BOXES_COUNT][CMD_ARG_OPT_FULL]
        short_arg_mode = CMD_ARGS[CMD_ARG_DETECTION_BOXES_COUNT][CMD_ARG_OPT_SHORT]
        parser.add_argument(
            short_arg_mode, full_arg_mode,
            nargs='?', type=int
        )
        
        full_arg_mode = CMD_ARGS[CMD_ARG_SCORE_THRESHOLD][CMD_ARG_OPT_FULL]
        short_arg_mode = CMD_ARGS[CMD_ARG_SCORE_THRESHOLD][CMD_ARG_OPT_SHORT]
        parser.add_argument(
            short_arg_mode, full_arg_mode,
            nargs='?', type=float, default=0.2
        )

        return parser

    def get_kwargs_for_execute(self):
        args = {}
        img_path = self.get_extracted_arg(CMD_ARG_IMG_PATH)
        if img_path:
            args['img_path'] = img_path
        
        ckpt = self.get_extracted_arg(CMD_ARG_CKPT)
        if ckpt:
            args['ckpt'] = ckpt
        
        boxes_cnt = self.get_extracted_arg(CMD_ARG_DETECTION_BOXES_COUNT)
        if boxes_cnt:
            args['boxes_count'] = boxes_cnt
        
        score_threshold = self.get_extracted_arg(CMD_ARG_SCORE_THRESHOLD)
        if score_threshold:
            args['score_threshold'] = score_threshold

        return args
    
def execute_show(img_path, ckpt=None, boxes_count=1, score_threshold=0.2):
    _, image_np_with_detections = execute(img_path, ckpt, boxes_count, score_threshold)
    plt.imshow(cv2.cvtColor(image_np_with_detections, cv2.COLOR_BGR2RGB))
    plt.savefig('detection_result.png')
    plt.show()

def execute(img_path, boxes_count=1, score_threshold=0.2, ckpt=None):
    config_loader = PipelineConfigLoader(
        config.get_reader().get_value(config.PRETRAINED_MODEL_NAME),
        config.get_reader().get_value(config.TRAINED_MODEL_NAME)
    )
    
    pipeline_config_path = config_loader.get_trained_config_path()
    ckpt_path = config_loader.get_trained_model_dir()
    label_map_path = get_label_map_path()

    configs = config_util.get_configs_from_pipeline_file(pipeline_config_path)
    detection_model = model_builder.build(model_config=configs['model'], is_training=False)

    if not ckpt:
        last_ckpt = sorted(glob.glob(os.path.join(ckpt_path, 'ckpt-*')))[-1]
        ckpt_regex = re.compile(r'(ckpt-\d+)')
        ckpt = ckpt_regex.findall(last_ckpt)[-1]
    
    model_checkpoint = tf.compat.v2.train.Checkpoint(model=detection_model)
    model_checkpoint.restore(os.path.join(ckpt_path, ckpt)).expect_partial()

    @tf.function
    def detect_fn(image):
        image, shapes = detection_model.preprocess(image)
        prediction_dict = detection_model.predict(image, shapes)
        detections = detection_model.postprocess(prediction_dict, shapes)
        return detections
    
    category_index = label_map_util.create_category_index_from_labelmap(label_map_path)

    img = cv2.imread(img_path)
    image_np = np.array(img)

    input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
    detections = detect_fn(input_tensor)

    num_detections = int(detections.pop('num_detections'))
    detections = {key: value[0, :num_detections].numpy()
                for key, value in detections.items()}
    detections['num_detections'] = num_detections

    # detection_classes should be ints.
    label_id_offset = 1
    detections['detection_classes'] = detections['detection_classes'].astype(np.int64) + label_id_offset
    detections['detection_scores'] = detection_scores_to_percentages(detections['detection_scores'])

    image_np_with_detections = image_np.copy()

    viz_utils.visualize_boxes_and_labels_on_image_array(
                image_np_with_detections,
                detections['detection_boxes'],
                detections['detection_classes'],
                detections['detection_scores'],
                category_index,
                use_normalized_coordinates=True,
                max_boxes_to_draw=boxes_count,
                min_score_thresh=score_threshold,
                agnostic_mode=False, )
    
    return detections, image_np_with_detections

if __name__ == '__main__':
    args_extractor = DetectArgumentExtractor()
    kwargs = args_extractor.get_kwargs_for_execute()
    execute_show(**kwargs)

