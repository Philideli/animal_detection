from .general import \
    MODE_SILENT as _MODE_SILENT, MODE_VERBOSE as _MODE_VERBOSE, \
    VERIFY_BOTH as _VER_BO, VERIFY_NONE as _VER_NO, VERIFY_AFTER as _VER_AF, VERIFY_BEFORE as _VER_BE

# +--------------------+
# | Common definitions |
# +--------------------+

CMD_ARG_OPT_FULL = 'full'
CMD_ARG_OPT_SHORT = 'short'

# +------------------------------------+
# | Command line arguments and options |
# +------------------------------------+

# +-~-~-~-+ mode +-~-~-~-+

CMD_ARG_MODE = 'mode'

CMD_MODE_ARG_TO_VAL_MAP = {
    'verbose': _MODE_VERBOSE,
    'silent': _MODE_SILENT
}

# +-~-~-~-+

# +-~-~-~-+ verification +-~-~-~-+

CMD_ARG_VERIFY = 'verify'

CMD_VERIFY_ARG_TO_VAL_MAP = {
    'both': _VER_BO,
    'none': _VER_NO,
    'after': _VER_AF,
    'before': _VER_BE
}

# +-~-~-~-+

# +-~-~-~-+ split ration +-~-~-~-+

CMD_ARG_SPLIT_RATIO = 'split_ratio'

# +-~-~-~-+

# +-~-~-~-+ number of training steps +-~-~-~-+

CMD_ARG_NUM_TRAIN_STEPS = 'num_train_steps'

# +-~-~-~-+

# +-~-~-~-+ save training checkpoints every n steps +-~-~-~-+

CMD_ARG_CHECKPOINT_EVERY_N = 'checkpoint_every_n'

# +-~-~-~-+

# +-~-~-~-+ model name (for training / eval / detection) +-~-~-~-+

CMD_ARG_MODEL_NAME = 'model_name'

# +-~-~-~-+

# +-~-~-~-+ +-~-~-~-+

CMD_ARG_IMG_PATH = 'image_path'

# +-~-~-~-+

# +-~-~-~-+ +-~-~-~-+

CMD_ARG_CKPT = 'ckpt'

# +-~-~-~-+

# +-~-~-~-+ +-~-~-~-+

CMD_ARG_DETECTION_BOXES_COUNT = 'boxes_cnt'

# +-~-~-~-+

# +-~-~-~-+ +-~-~-~-+

CMD_ARG_SCORE_THRESHOLD = 'score_threshold'

# +-~-~-~-+

CMD_ARGS = {
    CMD_ARG_MODE: {
        CMD_ARG_OPT_FULL: '--mode',
        CMD_ARG_OPT_SHORT: '-m'
    },
    CMD_ARG_VERIFY: {
        CMD_ARG_OPT_FULL: '--verify',
        CMD_ARG_OPT_SHORT: '-v',
    },
    CMD_ARG_SPLIT_RATIO: {
        CMD_ARG_OPT_FULL: '--split_ratio',
        CMD_ARG_OPT_SHORT: '-sr',
    },
    CMD_ARG_NUM_TRAIN_STEPS: {
        CMD_ARG_OPT_FULL: '--num_train_steps',
        CMD_ARG_OPT_SHORT: '-nts',
    },
    CMD_ARG_CHECKPOINT_EVERY_N: {
        CMD_ARG_OPT_FULL: '--checkpoint_every_n',
        CMD_ARG_OPT_SHORT: '-cen',
    },
    CMD_ARG_MODEL_NAME: {
        CMD_ARG_OPT_FULL: '--model-name',
        CMD_ARG_OPT_SHORT: '-mn',
    },
    CMD_ARG_IMG_PATH: {
        CMD_ARG_OPT_FULL: '--image-path',
        CMD_ARG_OPT_SHORT: '-ip',
    },
    CMD_ARG_CKPT: {
        CMD_ARG_OPT_FULL: '--ckpt',
        CMD_ARG_OPT_SHORT: '-ck',
    },
    CMD_ARG_DETECTION_BOXES_COUNT: {
        CMD_ARG_OPT_FULL: '--boxes-count',
        CMD_ARG_OPT_SHORT: '-bc',
    },
    CMD_ARG_SCORE_THRESHOLD: {
        CMD_ARG_OPT_FULL: '--score-threshold',
        CMD_ARG_OPT_SHORT: '-st',
    },
}
