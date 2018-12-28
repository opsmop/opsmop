# Copyright 2018 Michael DeHaan LLC, <michael@michaeldehaan.net>
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import io
import os
import shutil
import subprocess

from opsmop.callbacks.callbacks import Callbacks
from opsmop.core.common import memoize
from opsmop.core.result import Result


class Command(object):

    """
    A Command represents a re-executable representation of a shelll command.
    Once constructed, it is not active until "execute" is called, and "execute"
    returns an "opsmop.core.result.Result" object.
    """

    __slots__ = [ 'provider', 'cmd', 'timeout', 'echo', 'loud', 'fatal', 'input_text', 'env', 'ignore_lines', 'primary' ]

    def __init__(self, cmd, provider, env=None, input_text=None, timeout=None, echo=True, loud=False, fatal=False, ignore_lines=None, primary=False):

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
        ignore_lines: don't echo any lines starting with these items (takes a list of strings)
        primary: if True, this command invocation is the sole purpose of the provider (example: the shell module) and failure status be controlled by ignore_errors/failed_when/etc.
        """
        self.cmd = cmd
        self.provider = provider
        self.timeout = timeout
        self.loud = loud
        self.echo = echo
        self.fatal = fatal
        self.input_text = input_text
        self.env = env
        self.ignore_lines = ignore_lines
        self.primary = primary

    def to_dict(self):
        return dict(cls=self.__class__.__name__, cmd=self.cmd, timeout=self.timeout, env=self.env)

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

        Callbacks().on_execute_command(self.provider, self)
        
        command = self.cmd
        timeout_cmd = self.get_timeout()

        shell = True
        if type(command) == list:
            if self.timeout and timeout_cmd:
                command.insert(0, str(self.timeout))
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
            if (self.echo or self.loud) and (not self.ignore_lines or not self.should_ignore(line)):
                Callbacks().on_command_echo(self.provider, line)
            output = output + line
        if output.strip() == "":
            Callbacks().on_command_echo(self.provider, "(no output)")


        process.wait()

        res = None
        rc = process.returncode
        if rc != 0:
            res = Result(self.provider, rc=rc, data=output, fatal=self.fatal, primary=self.primary)
        else:
            res = Result(self.provider, rc=rc, data=output, fatal=False, primary=self.primary)
        # this callback will, depending on implementation, usually note fatal result objects and raise an exception
        Callbacks().on_command_result(self.provider, res)
        return res

    def should_ignore(self, line):
        # used for ignoring output on the console like "(Reading database 20% ...)" which is common for 'apt'
        # this may be modified to also do regular expressions in the future.
        for x in self.ignore_lines:
            if line.startswith(x):
                return True
        return False
