import argparse
import subprocess
import sys
import os

from animal_detection.common import config
from animal_detection.common.cmd import CmdArgumentExtractor
from animal_detection.constants.cmd import *
from animal_detection.constants.general import *
from animal_detection.constants.paths import *
from animal_detection.setup.verify import verify_tfod_api, verify_pretrained_model

INSTALL_TFOD_API_SCRIPT_WINDOWS = os.path.join(SETUP_PKG_PATH, 'install_tfod_api.bat')
INSTALL_TFOD_API_SCRIPT_LINUX = os.path.join(SETUP_PKG_PATH, 'install_tfod_api.sh')

PT_MODEL_LOAD_SCRIPT_WINDOWS = os.path.join(SETUP_PKG_PATH, 'load_pretrained_model.bat')
PT_MODEL_LOAD_SCRIPT_LINUX = os.path.join(SETUP_PKG_PATH, 'load_pretrained_model.sh')


class SetupArgumentExtractor(CmdArgumentExtractor):

    @staticmethod
    def get_parser():
        description = \
            'Script which prepares the workspace for all other activities' + \
            'like training, evaluation and object detection'
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

        full_arg_mode = CMD_ARGS[CMD_ARG_VERIFY][CMD_ARG_OPT_FULL]
        short_arg_mode = CMD_ARGS[CMD_ARG_VERIFY][CMD_ARG_OPT_SHORT]
        parser.add_argument(
            short_arg_mode, full_arg_mode,
            nargs='?', type=str,
            choices=list(CMD_VERIFY_ARG_TO_VAL_MAP.keys()),
        )
        return parser

    def get_kwargs_for_execute(self):
        args = {}
        mode_value = self.get_extracted_arg(CMD_ARG_MODE)
        if mode_value:
            args['mode'] = CMD_MODE_ARG_TO_VAL_MAP[mode_value]

        verify_value = self.get_extracted_arg(CMD_ARG_VERIFY)
        if verify_value:
            args['verify'] = CMD_VERIFY_ARG_TO_VAL_MAP[verify_value]

        return args


def install_tfod_api(mode=MODE_DEFAULT, verify=VERIFY_DEFAULT):
    tfod_api_path = config.get_reader().get_value(config.TFOD_API_INSTALL_DIRECTORY)
    # we check before if necessary and if tfod api is already installed
    # we don't need to do anything
    should_verify = (verify in [VERIFY_BEFORE, VERIFY_BOTH])
    if should_verify and verify_tfod_api(ENV_OS, tfod_api_path, mode == MODE_VERBOSE):
        return True
    # if not installed, we continue

    install_script = \
        INSTALL_TFOD_API_SCRIPT_WINDOWS if ENV_OS == OS_WINDOWS else INSTALL_TFOD_API_SCRIPT_LINUX

    args = [install_script, tfod_api_path]
    if ENV_OS == OS_LINUX:
        args = ['bash'] + args
    stdout = subprocess.DEVNULL if mode == MODE_SILENT else sys.stdout
    process = subprocess.Popen(args, stdout=stdout)
    _ = process.communicate()
    exitcode = process.returncode
    if exitcode != 0:
        raise subprocess.SubprocessError

    # check after installation if necessary (recommended)
    if verify in [VERIFY_AFTER, VERIFY_BOTH]:
        return verify_tfod_api(ENV_OS, tfod_api_path, mode == MODE_VERBOSE)

    # otherwise we assume everything was installed
    return True


def load_pretrained_model(mode=MODE_DEFAULT, verify=VERIFY_DEFAULT):
    pt_models_dir = os.path.abspath(
        config.get_reader().get_value(config.PRETRAINED_MODELS_DIRECTORY)
    )
    model_name = config.get_reader().get_value(config.PRETRAINED_MODEL_NAME)
    model_url = config.get_reader().get_value(config.PRETRAINED_MODEL_DOWNLOAD_LINK)
    # we check before if necessary and if model is already loaded
    # we don't need to do anything
    should_verify = (verify in [VERIFY_BEFORE, VERIFY_BOTH])
    if should_verify and verify_pretrained_model(pt_models_dir, model_name, mode == MODE_VERBOSE):
        return True
    # if not installed, we continue

    install_script = \
        PT_MODEL_LOAD_SCRIPT_WINDOWS if ENV_OS == OS_WINDOWS else PT_MODEL_LOAD_SCRIPT_LINUX

    args = [install_script, pt_models_dir, model_name, model_url]
    if ENV_OS == OS_LINUX:
        args = ['bash'] + args
    stdout = subprocess.DEVNULL if mode == MODE_SILENT else sys.stdout
    process = subprocess.Popen(args, stdout=stdout)
    _ = process.communicate()
    exitcode = process.returncode
    if exitcode != 0:
        raise subprocess.SubprocessError

    # check after loading if necessary (recommended)
    if verify in [VERIFY_AFTER, VERIFY_BOTH]:
        return verify_pretrained_model(pt_models_dir, model_name, mode == MODE_VERBOSE)

    # otherwise we assume everything was loaded
    return True


def execute(mode=MODE_DEFAULT, verify=VERIFY_DEFAULT):
    try:
        success = install_tfod_api(mode, verify)
        if not success:
            raise ValueError
    except (subprocess.SubprocessError, ValueError):
        if mode == MODE_VERBOSE:
            print('Installation of TFOD API failed')
        return False

    try:
        success = load_pretrained_model(mode, verify)
        if not success:
            raise ValueError
    except (subprocess.SubprocessError, ValueError):
        if mode == MODE_VERBOSE:
            print('Loading of pretrained model failed')
        return False

    return True


if __name__ == '__main__':
    args_extractor = SetupArgumentExtractor()
    kwargs = args_extractor.get_kwargs_for_execute()
    execute(**kwargs)
