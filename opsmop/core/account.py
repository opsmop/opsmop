# FIXME: this (for sudo, etc) isn't implemented yet.  What we would want to do is track the account context and prefix any commands with sudo -u
# is assumed opsmop would already be run as sudo

from opsmop.common.resource import Resource

class Account(Resource):

    """
    The Account object will be used when passed to 'sudo' clauses of statements.
    """
    
    pass