from opsmop.core.common import memoize
import os
import toml

LOCAL_CONFIG = "~/.opsmop/defaults.toml"
GLOBAL_CONFIG = "/etc/opsmop/defaults.toml"

DEFAULT_SSH_USERNAME = 'opsmop'
DEFAULT_SSH_PASSWORD = 'opsmop'
DEFAULT_SUDO_USERNAME = 'root'
DEFAULT_SUDO_PASSWORD = None
DEFAULT_SSH_CHECK_HOST_KEYS = 'ignore'

class UserDefaults(object):

    @classmethod
    @memoize
    def settings(cls):
        f1 = os.path.expanduser(os.path.expandvars(LOCAL_CONFIG))
        f2 = GLOBAL_CONFIG
        data = dict()
        if os.path.exists(f1):
            return toml.load(f1)
        elif os.path.exists(f2):
            return toml.load(f2)
        return data

    @classmethod
    def _extract(cls, category, key, default):
        settings = cls.settings()
        if category in settings:
            return settings[category].get(key, default)
        return default

    @classmethod
    def ssh_password(cls):
        pw = cls._extract('ssh', 'password', DEFAULT_SSH_PASSWORD)
        if not pw:
            return None
        return pw

    @classmethod
    def ssh_username(cls):
        return cls._extract('ssh', 'username', DEFAULT_SSH_USERNAME)

    @classmethod
    def ssh_check_host_keys(cls):
        return cls._extract('ssh', 'check_host_keys', DEFAULT_SSH_CHECK_HOST_KEYS)

    @classmethod
    def sudo_username(cls):
        return cls._extract('sudo', 'username', DEFAULT_SUDO_USERNAME)

    @classmethod
    def sudo_password(cls):
        pw = cls._extract('sudo', 'password', DEFAULT_SUDO_PASSWORD)
        if not pw:
            return None
        return pw

    @classmethod
    def python_path(cls):
        # this is the default remote python path and is mostly intended to be
        # set on inventory variables, not in the config, but technically can still
        # have a default here.
        return cls._extract('python', 'python_path', '/usr/bin/python3')

    @classmethod
    def max_workers(cls):
        # number of simultaneous workers during connection attempts
        return cls._extract('tuning', 'max_workers', 8)
        
    @classmethod
    def log_path(cls):
        return os.path.expanduser(cls._extract('log', 'path', '~/.opsmop/opsmop.log'))

    @classmethod
    def log_format(cls):
        return cls._extract('log', 'format', "%(asctime)s %(message)s")