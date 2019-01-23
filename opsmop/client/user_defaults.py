import getpass
import os
from opsmop.core.common import memoize

# provides a lot of defaults the application uses.  These should, in the future
# be configurable through the environment

@memoize
def get_user():
    return getpass.getuser()

DEFAULT_SSH_PASSWORD = None
DEFAULT_SUDO_USERNAME = 'root'
DEFAULT_SUDO_PASSWORD = None
DEFAULT_SSH_CHECK_HOST_KEYS = 'ignore'
DEFAULT_PYTHON = '/usr/bin/python3'
DEFAULT_LOG_PATH = '~/.opsmop/opsmop.log'
DEFAULT_LOG_FORMAT = "%(asctime)s %(message)s"

class UserDefaults(object):

    @classmethod
    def ssh_password(cls):
        return DEFAULT_SSH_PASSWORD

    @classmethod
    def ssh_username(cls):
        return get_user()

    @classmethod
    def ssh_check_host_keys(cls):
        return DEFAULT_SSH_CHECK_HOST_KEYS

    @classmethod
    def sudo_username(cls):
        return DEFAULT_SUDO_USERNAME

    @classmethod
    def sudo_password(cls):
        return DEFAULT_SUDO_PASSWORD

    @classmethod
    def python_path(cls):
        return DEFAULT_PYTHON
        
    @classmethod
    def max_workers(cls):
        # FIXME: load this from the environment?
        return 16
        
    @classmethod
    def log_path(cls):
        # FIXME: load this from the environment?
        return DEFAULT_LOG_PATH

    @classmethod
    def log_format(cls):
        return DEFAULT_LOG_FORMAT
        