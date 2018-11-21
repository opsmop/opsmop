import io
import os
import shutil
import subprocess

from opsmop.core.common import memoize
from opsmop.core.result import Result


class Command(object):

    """
    A Command represents a re-executable representation of a shelll command.
    Once constructed, it is not active until "execute" is called, and "execute"
    returns an "opsmop.core.result.Result" object.
    """

    __slots__ = [ 'provider', 'cmd', 'timeout', 'echo', 'loud', 'fatal', 'input_text', 'env' ]

    def __init__(self, cmd, provider=None, env=None, input_text=None, timeout=None, echo=True, loud=False, fatal=False):

        """
        Constructs but does not execute a command.

        cmd: a string or array of arguments including the command name. If an array is provided the shell will be bypassed.
        provider: a required reference to the provider class. The Command() class cannot be used seperately.
        env: an optional dict of environment variables to pass to the calling command
        input_text: any text to feed to standard input, if any
        timeout: the command will be killed after this many seconds
        echo: whether to show the command names + return codes + output on the screen using whatever callback class is set in the system
        fatal: whether any errors should fail the resource execution
        loud: whether to ignore 'quiet' preferences for just the output (but not command name or return codes)
        """
        assert provider is not None
        self.provider = provider
        self.cmd = cmd
        self.timeout = timeout
        self.loud = loud
        self.echo = echo
        self.fatal = fatal
        self.input_text = input_text
        self.env = env

    @memoize
    def get_timeout(self):
        """
        Returns the name of the timeout command, if present
        """
        t1 = shutil.which('timeout')
        if t1:
            return t1
        t2 = shutil.which('gtimeout')
        if t2:
            return t2
        return None


    def execute(self):
        """
        Execute a command (a list or string) with input_text as input, appending
        the output of all commands to the build log.

        This code was derived from http://vespene.io/ though is slightly different
        because there are no database objects.
        """

        context = self.provider.context()
        context.on_execute_command(self)
        
        command = self.cmd
        timeout_cmd = self.get_timeout()

        shell = True
        if type(command) == list:
            if self.timeout and timeout_cmd:
                command.insert(0, self.timeout)
                command.insert(0, timeout_cmd)
            shell = False
        else:
            if self.timeout and timeout_cmd:
                command = "%s %s %s" % (timeout_cmd, self.timeout, command)

        # keep SSH-agent working for executed commands
        sock = os.environ.get('SSH_AUTH_SOCK', None)
        if self.env and sock:
            self.env['SSH_AUTH_SOCK'] = sock

        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=shell, env=self.env)

        if self.input_text is None:
            self.input_text = ""

        stdin = io.TextIOWrapper(
            process.stdin,
            encoding='utf-8',
            line_buffering=True,
        )
        stdout = io.TextIOWrapper(
            process.stdout,
            encoding='utf-8',
        )
        stdin.write(self.input_text)
        stdin.close()

        output = ""
        for line in stdout:
            if self.echo or self.loud:
                context.on_command_echo(line)
            output = output + line
        if output.strip() == "":
            context.on_command_echo("(no output)")


        process.wait()

        res = None
        rc = process.returncode
        if rc != 0:
            res = Result(provider=self.provider, rc=rc, data=output, fatal=self.fatal)
        else:
            res = Result(provider=self.provider, rc=rc, data=output, fatal=False)
        # this callback will, depending on implementation, usually note fatal result objects and raise an exception
        context.on_command_result(res)
        return res
