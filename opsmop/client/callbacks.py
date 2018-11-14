import sys
from opsmop.core.callback import BaseCallback

# FIXME: this is moving in the right direction but still needs to get refactored a good bit

POLICY_INDENT=1
RESOURCE_INDENT=2
RESOURCE_RESULT_INDENT=3
COMMAND_INDENT=3
COMMAND_RESULT_INDENT=4
COMMAND_ECHO_INDENT=4
INDENT="  "


class CliCallbacks(BaseCallback):

    """
    Callback class for the default CLI implementation.
    Improvements are welcome.
    """

    def __init__(self):
        super()
        self.phase = None
        self.dry_run = False

        # keep a list of resource counters
        # FIXME: we should know how many we validated, which gives a percentage - DO THIS NEXT!



    def on_conditions(self, conditions):
        self.i3("conditions: %s" % conditions)
                
    def on_command_echo(self, echo):
        if echo == "":
            return
        self.i4("| %s" % echo.rstrip())

    def on_echo(self, echo):
        self.i4("| %s" % echo)

    def on_execute_command(self, command):
        # FIXME: this looks redundant with on_begin_command, is the other called?
        if command.echo:
           self.i4("> %s" % command.cmd)

    def on_plan(self, provider):
        self.i3("planning")
   
    def on_apply(self, provider):
        self.i3("applying")
    
    def on_planned_actions(self, provider, actions_planned):
        self.i4("actions planned: %s" % [ str(x) for x in actions_planned])

    def on_taken_actions(self, provider, actions_taken):
        self.i4("actions taken: %s" % [ str(x) for x in actions_taken])

    def on_result(self, result):
        self.i3("= %s" % result)

    def on_command_result(self, result):
        self.i4("= %s" % result)
        # pay attention to self.context.category and 

    def on_skipped(self, skipped):
        self.i3("skipped: %s" % skipped)

    def on_resource(self, resource, is_handler):
        if not is_handler:
            self.i1("Resource: %s" % resource)
        else:
            self.i1("Handler: %s" % resource)

    def on_flagged(self, flagged):
        self.i3("flagged: %s" % flagged)

    def on_complete(self, policy):
        self.i1("complete!")
        self.summarize()

    def summarize(self):
        # FIXME: re-implement the counter table, but much cleaner
        pass

    def on_fatal(self):
        self.summarize()
        sys.exit(1)

    def on_all_policies_complete(self):
        pass

    def on_update_variables(self, variables):
        for (k,v) in variables.items():
            self.on_echo("%s => %s" % (k,v))

    def i1(self, msg):
        # indent methods
        self._indent(0, msg)

    def i2(self, msg):
        self._indent(1, msg)

    def i3(self, msg):
        self._indent(2, msg)

    def i4(self, msg):
        self._indent(3, msg)

    def i5(self, msg):
        self._indent(4, msg)
    
    def _indent(self, level, msg):
        spc = "     " * level
        print("%s%s" % (spc, msg))


