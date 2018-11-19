import sys
from opsmop.core.callback import BaseCallback

INDENT="  "

class CliCallbacks(BaseCallback):

    """
    Callback class for the default CLI implementation.
    Improvements are welcome.
    """

    def __init__(self):
        super()
        self.dry_run = False
        self.role = None
        self.last_role = None
        self.phase = None
        self.count = 0

    def banner(self, msg, big=False):
        msg_len = len(msg)
        sep = None
        if big:
            sep = "=" * msg_len
        else:
            sep = "-" * msg_len
        self.i1(sep)
        self.i1(msg)
        if big:
            self.i1(sep)

    def on_conditions(self, conditions):
        if len(conditions) > 0:
            self.i3("conditions:")
            self.i5(str(conditions))

    def on_command_echo(self, echo):
        if echo == "":
            return
        self.i5("| %s" % echo.rstrip())

    def on_echo(self, echo):
        self.i5("| %s" % echo)

    def on_execute_command(self, command):
        if command.echo:
           self.i5("# %s" % command.cmd)

    def on_plan(self, provider):
        self.provider = provider
        self.phase="plan"
        if self.provider.skip_plan_stage():
            return
        self.i3("planning...")

    def on_apply(self, provider):
        self.i3(provider.verb())
        self.phase="apply"
    
    def on_planned_actions(self, provider, actions_planned):
        if self.provider.skip_plan_stage():
            return
        self.provider = provider
        self.i3("planned:")
        for x in actions_planned:
            self.i5(f"| {x}")

    def on_taken_actions(self, provider, actions_taken):
        if provider.skip_plan_stage():
            return
        self.provider = provider
        taken = sorted([ str(x) for x in provider.actions_taken ])
        planned = sorted([ str(x) for x in provider.actions_planned ])
        if (taken != planned):
            self.i4("ERROR: actions planned do not equal actions taken: %s" % taken)
            self.on_fatal()

    def on_result(self, result):
        self.i3(str(result))

    def on_command_result(self, result):
        self.i5("= %s" % result)
        # pay attention to self.context.category and 

    def on_evaluation_failed(self, expr):
        self.i3("conditional evaluation error, unable to evaluate expression:")
        self.i5("| %s" % expr)
        self.fatal()

    def on_skipped(self, skipped):
        self.on_resource(skipped, False)
        self.i3("skipped")

    def on_resource(self, resource, is_handler):
        self.i1("")
        if (self.role != self.last_role) or (self.last_role is None):
            self.last_role = self.role
            msg = f"{self.role}"
            self.banner(msg, big=True)
            self.i1("")
            self.count = 1
        self.banner(f"{self.count}. {resource}")
        self.i1("")
        self.count = self.count + 1
        if is_handler:
            self.i3("handler for:")
            self.i5("| %s" % resource.handles)

    def on_flagged(self, flagged):
        self.i3("flagged: %s" % flagged)

    def on_complete(self, policy):
        self.i1("")
        self.i1("complete!")
        self.summarize()

    def on_role(self, role):
        self.role = role

    def summarize(self):
        # TODO: reimplement the counter and percentages summary
        pass

    def on_fatal(self, msg=None):
        if msg:
            self.i1("FAILED: %s" % msg)
        else:
            self.i1("FAILED")
        self.summarize()
        # TODO: we should not exit here but raise an Exception, Api and PullApi will want to catch it.
        # TODO: further, run_callbacks in Context() should catch any exceptions from *ALL* callbacks and re-raise
        sys.exit(1)

    def on_all_policies_complete(self):
        pass

    def on_update_variables(self, variables):
        self.i3("registered:")
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
        spc = INDENT * level
        print("%s%s" % (spc, msg))


