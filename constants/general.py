from platform import system

# +-----------------+
# | Execution modes |
# +-----------------+

MODE_VERBOSE = 'mode_verbose'
MODE_SILENT = 'mode_silent'
MODE_DEFAULT = MODE_VERBOSE

# +--------------+
# | Verification |
# +--------------+

VERIFY_BOTH = 'verify_both'
VERIFY_NONE = 'verify_none'
VERIFY_AFTER = 'verify_after'
VERIFY_BEFORE = 'verify_before'
VERIFY_DEFAULT = VERIFY_BOTH

# +----------------+
# | OS information |
# +----------------+

OS_WINDOWS = 'windows'
OS_LINUX = 'linux'
ENV_OS = system().lower()

