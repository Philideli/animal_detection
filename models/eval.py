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

from animal_detection.models.train import PipelineConfigLoader


LIGHT_BATCH_SIZE = 4
EXTREME_BATCH_SIZE = 8  # please only use on a performant pc


class EvalArgumentParser(CmdArgumentExtractor):
    # num_train_steps

    @staticmethod
    def get_parser():
        description = \
            'Script which evaluates the trained model'
        parser = argparse.ArgumentParser(
            description=description
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

        return args

def run_eval_script(
    config_loader: PipelineConfigLoader,
    mode=MODE_DEFAULT
):
    tfod_api_dir = config.get_reader().get_value(TFOD_API_INSTALL_DIRECTORY)
    eval_script = os.path.join(
        os.path.abspath(tfod_api_dir),
        'object_detection',
        'model_main_tf2.py'
    )

    model_dir_arg = f'--model_dir={config_loader.get_trained_model_dir()}'
    config_path = config_loader.get_trained_config_path()
    pipeline_config_path_arg = f'--pipeline_config_path={config_path}'
    checkpoint_path_arg = f'--checkpoint_dir={config_loader.get_trained_model_dir()}'
    args = [
        sys.executable,
        eval_script,
        model_dir_arg,
        pipeline_config_path_arg,
        checkpoint_path_arg,
    ]
    
    if (mode == MODE_VERBOSE):
        print('execute command:')
        print(str.join(' ', args))

    stdout = subprocess.DEVNULL if mode == MODE_SILENT else sys.stdout
    process = subprocess.Popen(args, stdout=stdout)
    _ = process.communicate()
    exitcode = process.returncode
    if exitcode != 0:
        raise subprocess.SubprocessError

    return True


def execute(mode=MODE_DEFAULT):
    config_loader = PipelineConfigLoader(
        config.get_reader().get_value(config.PRETRAINED_MODEL_NAME),
        config.get_reader().get_value(config.TRAINED_MODEL_NAME)
    )
    try:
        success = run_eval_script(config_loader, mode)
        if not success:
            raise ValueError
    except (subprocess.SubprocessError, ValueError):
        if mode == MODE_VERBOSE:
            print('Evaluation could not be finished')
        return False


if __name__ == '__main__':
    args_extractor = EvalArgumentParser()
    kwargs = args_extractor.get_kwargs_for_execute()
    execute(**kwargs)

