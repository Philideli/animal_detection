import argparse
import os
import shutil
import subprocess
import sys

from animal_detection.common.config import TFOD_API_INSTALL_DIRECTORY
from animal_detection.common.cmd import CmdArgumentExtractor
from animal_detection.constants.general import MODE_DEFAULT, MODE_VERBOSE, MODE_SILENT
from animal_detection.constants.cmd import *
from animal_detection.common import config
from animal_detection.data.preparation import \
    get_label_map_path, get_eval_record_path, get_train_record_path
import tensorflow as tf
from object_detection.protos import pipeline_pb2
from object_detection.utils import label_map_util
from google.protobuf import text_format


LIGHT_BATCH_SIZE = 4
EXTREME_BATCH_SIZE = 8  # please only use on a performant pc


class TrainArgumentExtractor(CmdArgumentExtractor):
    # num_train_steps

    @staticmethod
    def get_parser():
        description = \
            'Script which prepares the raw dataset from perception for training'
        parser = argparse.ArgumentParser(
            description=description
        )
        full_arg_mode = CMD_ARGS[CMD_ARG_NUM_TRAIN_STEPS][CMD_ARG_OPT_FULL]
        short_arg_mode = CMD_ARGS[CMD_ARG_NUM_TRAIN_STEPS][CMD_ARG_OPT_SHORT]
        parser.add_argument(
            short_arg_mode, full_arg_mode,
            nargs='?', type=int, default=1000
        )
        full_arg_mode = CMD_ARGS[CMD_ARG_CHECKPOINT_EVERY_N][CMD_ARG_OPT_FULL]
        short_arg_mode = CMD_ARGS[CMD_ARG_CHECKPOINT_EVERY_N][CMD_ARG_OPT_SHORT]
        parser.add_argument(
            short_arg_mode, full_arg_mode,
            nargs='?', type=int, default=1000
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
        train_steps = self.get_extracted_arg(CMD_ARG_NUM_TRAIN_STEPS)
        if train_steps:
            args['num_train_steps'] = train_steps
        checkpoint_every_n = self.get_extracted_arg(CMD_ARG_CHECKPOINT_EVERY_N)
        if checkpoint_every_n:
            args['checkpoint_every_n'] = checkpoint_every_n


        return args


class PipelineConfigLoader:

    def __init__(self, pretrained_model, custom_model):
        self.pretrained_model = pretrained_model
        self.custom_model = custom_model
        self.config = None
        self.custom_config = None

    def get_pretrained_model_dir(self):
        pt_models_dir = config.get_reader().get_value(
            config.PRETRAINED_MODELS_DIRECTORY
        )
        return os.path.join(pt_models_dir, self.pretrained_model)

    def get_pretrained_config_path(self):
        return os.path.join(self.get_pretrained_model_dir(), 'pipeline.config')

    def get_trained_model_dir(self):
        trained_models_dir = config.get_reader().get_value(
            config.TRAINED_MODELS_DIRECTORY
        )
        return os.path.join(trained_models_dir, self.custom_model)

    def get_trained_config_path(self):
        return os.path.join(self.get_trained_model_dir(), 'pipeline.config')

    def copy_empty_pretrained_config(self):
        trained_model_dir = self.get_trained_model_dir()
        if not os.path.isdir(trained_model_dir):
            os.makedirs(trained_model_dir)
        shutil.copy(self.get_pretrained_config_path(), trained_model_dir)

    def load_config_from_pretrained_model(self):
        self.config = pipeline_pb2.TrainEvalPipelineConfig()
        with tf.io.gfile.GFile(self.get_pretrained_config_path(), 'r+') as pretrained_file:
            proto_str = pretrained_file.read()
            text_format.Merge(proto_str, self.config)

    def fill_config_with_data(
            self,
            starting_checkpoint_path,
            label_map_path,
            train_record_path,
            eval_record_path,
            num_classes=10,
            batch_size=4
    ):
        self.config.model.ssd.num_classes = num_classes
        self.config.train_config.batch_size = batch_size
        self.config.train_config.fine_tune_checkpoint = os.path.abspath(
            starting_checkpoint_path
        )
        self.config.train_config.fine_tune_checkpoint_type = "detection"
        self.config.train_input_reader.label_map_path = os.path.abspath(
            label_map_path
        )
        self.config.train_input_reader.tf_record_input_reader.input_path[:] = [
            os.path.abspath(train_record_path)
        ]
        self.config.eval_input_reader[0].label_map_path = label_map_path
        self.config.eval_input_reader[0].tf_record_input_reader.input_path[:] = [
            os.path.abspath(eval_record_path)
        ]

    def write_config_to_trained_model(self):
        try:
            trained_model_dir = self.get_trained_model_dir()
            if not os.path.isdir(trained_model_dir):
                os.makedirs(trained_model_dir)
            config_text = text_format.MessageToString(self.config)
            with tf.io.gfile.GFile(self.get_trained_config_path(), 'wb+') as trained_file:
                trained_file.write(config_text)
        except (IOError, OSError, FileNotFoundError):
            return False
        else:
            return True


def run_training_script(
        config_loader: PipelineConfigLoader,
        num_train_steps=1000,
        checkpoint_every_n=1000,
        mode=MODE_DEFAULT
):
    tfod_api_dir = config.get_reader().get_value(TFOD_API_INSTALL_DIRECTORY)
    training_script = os.path.join(
        os.path.abspath(tfod_api_dir),
        'object_detection',
        'model_main_tf2.py'
    )

    model_dir_arg = f'--model_dir={config_loader.get_trained_model_dir()}'
    config_path = config_loader.get_trained_config_path()
    pipeline_config_path_arg = f'--pipeline_config_path={config_path}'
    train_steps_arg = f'--num_train_steps={num_train_steps}'
    checkpoint_every_arg = f'--checkpoint_every_n={checkpoint_every_n}'
    args = [
        sys.executable,
        training_script,
        model_dir_arg,
        pipeline_config_path_arg,
        train_steps_arg,
        checkpoint_every_arg
    ]

    stdout = subprocess.DEVNULL if mode == MODE_SILENT else sys.stdout
    process = subprocess.Popen(args, stdout=stdout)
    _ = process.communicate()
    exitcode = process.returncode
    if exitcode != 0:
        raise subprocess.SubprocessError

    return True


def write_training_config(mode=MODE_DEFAULT):
    if mode == MODE_VERBOSE:
        print('loading pipeline config for training from the pretrained model...')

    config_loader = PipelineConfigLoader(
        config.get_reader().get_value(config.PRETRAINED_MODEL_NAME),
        config.get_reader().get_value(config.TRAINED_MODEL_NAME)
    )
    config_loader.load_config_from_pretrained_model()
    label_map_path = get_label_map_path()
    label_map = label_map_util.load_labelmap(label_map_path)
    label_map = label_map_util.get_label_map_dict(label_map)
    checkpoint_path = os.path.abspath(
        os.path.join(config_loader.get_pretrained_model_dir(), 'checkpoint', 'ckpt-0')
    )
    config_loader.fill_config_with_data(
        checkpoint_path,
        label_map_path,
        get_train_record_path(),
        get_eval_record_path(),
        len(label_map.keys()),
        LIGHT_BATCH_SIZE
    )
    success = config_loader.write_config_to_trained_model()

    if mode == MODE_VERBOSE:
        print(f'pipeline config {"" if success else "could not be "} loaded')

    return config_loader


def execute(num_train_steps=1000, checkpoint_every_n=1000, mode=MODE_DEFAULT):
    config_loader = write_training_config(mode)
    try:
        success = run_training_script(config_loader, num_train_steps, checkpoint_every_n, mode)
        if not success:
            raise ValueError
    except (subprocess.SubprocessError, ValueError):
        if mode == MODE_VERBOSE:
            print('Training could not be finished')
        return False


if __name__ == '__main__':
    args_extractor = TrainArgumentExtractor()
    kwargs = args_extractor.get_kwargs_for_execute()
    execute(**kwargs)

