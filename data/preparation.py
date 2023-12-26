import argparse

from animal_detection.common.cmd import CmdArgumentExtractor
from animal_detection.constants.cmd import *
from animal_detection.common.config import \
    RAW_DATASET_ANNOTATIONS_DIRNAME as ANNOTATIONS_DIRNAME, \
    RAW_DATASET_IMAGES_DIRNAME as IMAGES_DIRNAME, \
    RAW_DATASET_ANNOTATIONS_LIST_PATH as LIST_PATH
from animal_detection.common import config
import os
from animal_detection.data.processing import \
    OxfordRawDatasetClassDataReader, OxfordRawDatasetObjectDetectionReader, ProcessedDatasetWriter, write_label_map
from sklearn.model_selection import train_test_split
from animal_detection.constants.paths import \
    PROCESSED_DATASET_TRAIN_DIRNAME as TRAIN_DIRNAME, \
    PROCESSED_DATASET_EVAL_DIRNAME as EVAL_DIRNAME
from animal_detection.constants.general import MODE_DEFAULT, MODE_VERBOSE
import traceback
from typing import Tuple, List, Optional
from animal_detection.data.tf_records import TFRecordsGenerator
import pathlib

TF_RECORD_TRAIN = 'train.record'
TF_RECORD_EVAL = 'eval.record'
LABEL_MAP_FILENAME = 'label_map.pbtxt'


class DatasetPreparationArgumentExtractor(CmdArgumentExtractor):

    @staticmethod
    def get_parser():
        description = \
            'Script which prepares the raw dataset from perception for training'
        parser = argparse.ArgumentParser(
            description=description
        )
        full_arg_mode = CMD_ARGS[CMD_ARG_SPLIT_RATIO][CMD_ARG_OPT_FULL]
        short_arg_mode = CMD_ARGS[CMD_ARG_SPLIT_RATIO][CMD_ARG_OPT_SHORT]
        parser.add_argument(
            short_arg_mode, full_arg_mode,
            nargs='?', type=float, default=0.2
        )

        full_arg_mode = CMD_ARGS[CMD_ARG_MODE][CMD_ARG_OPT_FULL]
        short_arg_mode = CMD_ARGS[CMD_ARG_MODE][CMD_ARG_OPT_SHORT]
        parser.add_argument(
            short_arg_mode, full_arg_mode,
            nargs='?', type=str,
            choices=list(CMD_MODE_ARG_TO_VAL_MAP.keys()),
        )
        return parser

    def get_kwargs_for_execute(self):
        args = {}
        mode_value = self.get_extracted_arg(CMD_ARG_MODE)
        if mode_value:
            args['mode'] = CMD_MODE_ARG_TO_VAL_MAP[mode_value]

        split_ratio_value = self.get_extracted_arg(CMD_ARG_SPLIT_RATIO)
        if split_ratio_value:
            args['split_ratio'] = split_ratio_value

        return args


def get_dataset_name():
    return config.get_reader().get_value(config.DATASET_NAME)


def get_raw_dataset_dir():
    raw_dir = config.get_reader().get_value(config.RAW_DATASETS_DIRECTORY)
    dataset_name = get_dataset_name()
    return os.path.join(raw_dir, dataset_name)


def get_annotations_dir():
    dataset_dir = get_raw_dataset_dir()
    definitions_dirname = config.get_reader().get_value(ANNOTATIONS_DIRNAME)
    return os.path.join(dataset_dir, definitions_dirname)

def get_annotations_list_path():
    dataset_dir = get_raw_dataset_dir()
    path = config.get_reader().get_value(LIST_PATH)
    return os.path.join(dataset_dir, path)


def get_images_dir():
    dataset_dir = get_raw_dataset_dir()
    images_dirname = config.get_reader().get_value(IMAGES_DIRNAME)
    return os.path.join(dataset_dir, images_dirname)


def get_processed_dir():
    processed_datasets_dir = config.get_reader().get_value(config.PROCESSED_DATASETS_DIRECTORY)
    dataset_name = get_dataset_name()
    return os.path.join(processed_datasets_dir, dataset_name)


def get_train_data_dir():
    processed_dir = get_processed_dir()
    return os.path.join(processed_dir, TRAIN_DIRNAME)


def get_eval_data_dir():
    processed_dir = get_processed_dir()
    return os.path.join(processed_dir, EVAL_DIRNAME)


def get_train_record_path():
    processed_dir = get_processed_dir()
    return os.path.join(processed_dir, TF_RECORD_TRAIN)


def get_eval_record_path():
    processed_dir = get_processed_dir()
    return os.path.join(processed_dir, TF_RECORD_EVAL)


def get_label_map_path():
    processed_dir = get_processed_dir()
    return os.path.join(processed_dir, LABEL_MAP_FILENAME)


# use typing here for better IDE recommendations
def generate_processed_dataset(
        split_ratio: float = 0.2, mode: Optional[str] = MODE_DEFAULT
) -> Tuple[Optional[OxfordRawDatasetObjectDetectionReader], Optional[List], Optional[List]]:
    # noinspection PyBroadException
    try:
        if mode == MODE_VERBOSE:
            print('Reading raw dataset')

        class_info_reader = OxfordRawDatasetClassDataReader(get_annotations_list_path())
        class_df = class_info_reader.read_as_df()
        raw_dataset_reader = OxfordRawDatasetObjectDetectionReader(get_images_dir(), get_annotations_dir(), class_df)
        image_paths = raw_dataset_reader.get_image_paths(abs_path=True)
        images_train, images_eval = train_test_split(image_paths, test_size=split_ratio)

        if mode == MODE_VERBOSE:
            print('Successfully read raw dataset')

        if mode == MODE_VERBOSE:
            print('Writing processed dataset')

        train_writer = ProcessedDatasetWriter(get_train_data_dir())
        train_writer.clean_processed_data()
        train_writer.copy_to_destination(images_train)
        images_train = train_writer.get_processed_files()

        eval_writer = ProcessedDatasetWriter(get_eval_data_dir())
        eval_writer.clean_processed_data()
        eval_writer.copy_to_destination(images_eval)
        images_eval = eval_writer.get_processed_files()

        if mode == MODE_VERBOSE:
            print('Successfully wrote processed dataset')

        return raw_dataset_reader, images_train, images_eval
    except Exception:
        print('Could not generate the processed dataset')
        traceback.print_exc()
        return None, None, None


def generate_tf_records(raw_reader, images, images_dir, output_file, mode=MODE_DEFAULT):
    image_data = []
    if mode == MODE_VERBOSE:
        print('generate tf records from', images_dir)
    for image in images:
        filename = os.path.basename(image)
        filename_no_ext = pathlib.Path(filename).stem
        image_objects = raw_reader.get_objects_bounding_boxes(filename_no_ext)
        image_data += [{
            TFRecordsGenerator.IMAGE_FILENAME: filename,
            TFRecordsGenerator.IMAGE_OBJECTS: image_objects
        }]

    record_generator = TFRecordsGenerator(images_dir)
    record_generator.add_tf_examples(image_data)
    records_written = record_generator.write_records(output_file)

    if mode == MODE_VERBOSE:
        if records_written:
            print('records written successfully')
        else:
            print('records could not be written')

    return records_written


def execute(split_ratio=0.2, mode=MODE_DEFAULT):
    raw_reader, images_train, images_eval = \
        generate_processed_dataset(split_ratio, mode)
    if not (raw_reader or images_train or images_eval):
        print('could not generate processed dataset')
        return False

    if not write_label_map(raw_reader, get_label_map_path()):
        print('could not write label map')
        return False

    result_train = generate_tf_records(
        raw_reader, images_train, get_train_data_dir(),
        get_train_record_path(), mode
    )
    result_eval = generate_tf_records(
        raw_reader, images_eval, get_eval_data_dir(),
        get_eval_record_path(), mode
    )
    if not (result_train and result_eval):
        print('could not generate tf records')
        return False
    return True


if __name__ == '__main__':
    args_extractor = DatasetPreparationArgumentExtractor()
    kwargs = args_extractor.get_kwargs_for_execute()
    execute(**kwargs)
