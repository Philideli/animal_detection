from animal_detection.constants.general import OS_WINDOWS, ENV_OS, OS_LINUX
from animal_detection.constants.paths import SETUP_PKG_PATH
from animal_detection.common import config
import os
import subprocess
from animal_detection.common.config import TFOD_API_INSTALL_DIRECTORY

VERIFY_TFOD_API_SCRIPT_WINDOWS = os.path.join(
    SETUP_PKG_PATH, 'verify_scripts', 'verify_tfod_api_installation.bat'
)
VERIFY_TFOD_API_SCRIPT_LINUX = os.path.join(
    SETUP_PKG_PATH, 'verify_scripts', 'verify_tfod_api_installation.sh'
)


def verify_tfod_api(system, tfod_api_path, print_status=True):
    script = \
        VERIFY_TFOD_API_SCRIPT_WINDOWS if system == OS_WINDOWS else VERIFY_TFOD_API_SCRIPT_LINUX
    args = [script, tfod_api_path]
    if ENV_OS == OS_LINUX:
        args = ['bash'] + args
    log_filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'verify_log.txt')

    with open(log_filename, 'w+') as logfile:
        if print_status:
            print('Verifying if TFOD API is installed (correctly)...')
        exitcode = subprocess.call(args, stdout=logfile, stderr=logfile)

    with open(log_filename, 'r') as logfile:
        last_line = logfile.readlines()[-1]

    success = (exitcode == 0) and ('OK' in last_line)

    if os.path.exists(log_filename):
        os.remove(log_filename)

    if print_status:
        print(f'TFOD API is {"" if success else "NOT "}installed (correctly)')

    return success


def verify_pretrained_model(pretrained_models_dir, model_name, print_status=True):
    success = True

    if not os.path.isdir(pretrained_models_dir):
        success = False

    cur_pretrained_model_dir = os.path.join(
        pretrained_models_dir,
        model_name
    )
    if not os.path.isdir(cur_pretrained_model_dir):
        success = False

    checkpoints_dir = os.path.join(cur_pretrained_model_dir, 'checkpoint')
    if not os.path.isdir(checkpoints_dir):
        success = False

    checkpoints_file = os.path.join(checkpoints_dir, 'checkpoint')
    if not os.path.isfile(checkpoints_file):
        success = False

    pipeline_config_file = os.path.join(cur_pretrained_model_dir, 'pipeline.config')
    if not os.path.isfile(pipeline_config_file):
        success = False

    if print_status:
        print(f'Pretrained model was {"" if success else "NOT "}loaded (correctly)')

    return success


def execute():
    verify_tfod_api(
        ENV_OS,
        config.get_reader().get_value(TFOD_API_INSTALL_DIRECTORY)
    )
    verify_pretrained_model(
        config.get_reader().get_value(config.PRETRAINED_MODELS_DIRECTORY),
        config.get_reader().get_value(config.PRETRAINED_MODEL_NAME)
    )


if __name__ == '__main__':
    execute()
