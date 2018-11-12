import sys
import traceback

POLICY_INDENT=1
RESOURCE_INDENT=2
RESOURCE_RESULT_INDENT=3
COMMAND_INDENT=3
COMMAND_RESULT_INDENT=4
COMMAND_ECHO_INDENT=4
INDENT="  "

# FIXME: WARNING: this file is kind of a mess at the moment, but largely works.
# once stabilized, it will get cleaned up lots. 
# in particular, we a context object and less params to each event, and more
# standardization in callback event names

class Callbacks(object):

    """
    The callbacks class encapsulates CLI output, but also behavior. For instance, operations that
    recieve result objects may decide how to proceed with error handling by either logging, accumulating
    messages/state, or exiting the program.

    Individual comments describe each method.

    I'm not 100% happy with this interface so it is highly subject to change.
    Maybe I'd want a uniform "context" object to each callback and *possibly* less functions.
    """

    def __init__(self):
        """
        Just a default set of CLI callbacks.  Feel free to write alternate versions.
        """
        # modify messages slightly for resources vs handlers phases
        self.phase = None
        self.dry_run = False

        # keep a list of resource counters
        # FIXME: we should know how many we validated, which gives a percentage - DO THIS NEXT!

        self.resource_count = 0
        self.validated = []
        self.validated_handlers = []
        self.validated_resources = []
        self.processed = []
        self.successful = []
        self.successful_resources = []
        self.successful_handlers = []
        self.changed = []
        self.changed_resources = []
        self.changed_handlers = []
        self.skipped = []
        self.skipped_resources = []
        self.skipped_handlers = []
        self.failed = []
        self.failed_handlers = []
        self.failed_resources = []
        self.handlers = []

    def set_dry_run(self, value):
        self.dry_run = value

    def on_local_show(self, policy, data):
        """
        Show the parsed policy object as low-level JSON.  This is debug level stuff.
        """
        print("\n")
        print(json.dumps(data, indent=4)) # not the same indent
        print("\n")
    
    def on_resources_start(self, policy):
        """
        Signal processing of the resources tree (as opposed to the handlers tree)
        """
        self.phase = 'resource'

    def on_resource_begin(self, policy, resource):


        # FIXME: we need a quiet() method on the resource too?
        self.resource_count = self.resource_count + 1
        self.processed.append(resource)
        self.info("-----------------", indent=RESOURCE_INDENT)
        self.info("%d. %s" % (self.resource_count, resource), indent=RESOURCE_INDENT)
        # self.info("arguments: %s" % resource.kwargs, indent=RESOURCE_RESULT_INDENT) 

    def on_handlers_start(self, policy):
        """
        Signal processing of the handlers tree, which is conditional depending on what resources fired.
        """
        self.phase = 'handler'

    def on_policy_results(self, policy, results):
        """
        Called when the entire policy is done executing.
        Note - the CLI *CAN* run over multiple policies.

        If a failure on any policy should cause an exit, it should be coded that way here.
        """
        self.summarize()

    def on_validated(self, resource, handler=False):
        self.validated.append(resource)
        if handler:
            self.validated_handlers.append(resource)
        else:
            self.validated_resources.append(resource)

    def summarize(self):

        # FIXME: cleanup, have a seperate class do this calculation.


        self.info("resources:")
        self.info("scanned      | %s" % len(self.validated_resources), indent=POLICY_INDENT)
        self.info("ran          | %s" % len(self.successful_resources), indent=POLICY_INDENT)
        self.info("signaled     | %s" % len(self.handlers), indent=POLICY_INDENT)
        self.info("changed      | %s" % len(self.changed_resources), indent=POLICY_INDENT)
        self.info("skipped      | %s" % len(self.skipped_resources), indent=POLICY_INDENT)
        self.info("failed       | %s" % len(self.failed_resources), indent=POLICY_INDENT)

        exec_resources = len(self.successful_resources) + len(self.skipped_resources)
        total_resources = len(self.validated_resources)
        if total_resources == 0:
            percent_resources = 0
        else:
            percent_resources = 100*(exec_resources / float(total_resources))
        percent_resources = "%.2f" % percent_resources
        self.info("percentage   | {x}%".format(x=percent_resources), indent=POLICY_INDENT)
        self.info("")



        self.info("handlers:")
        self.info("scanned      | %s" % len(self.validated_handlers), indent=POLICY_INDENT)
        self.info("ran          | %s" % len(self.successful_handlers), indent=POLICY_INDENT)
        self.info("changed      | %s" % len(self.changed_handlers), indent=POLICY_INDENT)
        self.info("skipped      | %s" % len(self.skipped_handlers), indent=POLICY_INDENT)
        self.info("failed       | %s" % len(self.failed_handlers), indent=POLICY_INDENT)

        exec_handlers = len(self.successful_handlers) + len(self.skipped_handlers)
        total_handlers = len(self.validated_handlers)
        if total_handlers != 0:
            percent_handlers = 100*(exec_handlers / float(total_handlers))
        else:
            percent_handlers = 0
        percent_handlers = "%.2f" % percent_handlers
        self.info("percentage   | {x}%".format(x=percent_handlers), indent=POLICY_INDENT)

        self.info("")

        
        is_failed = (len(self.failed) > 0)

        if is_failed:
            self.info("** FAILED **", indent=POLICY_INDENT)
            self.info("")


    def on_actions_apply_begin(self, policy, resource, provider, actions):
        """
        We've figured out what we want to do to a resource, and are now doing it.
        """
        # FIXME: this next statement shouldn't run either if quiet.
        if provider.quiet():
            return
        what = [ str(x) for x in actions ]
        # FIXME: we need a stupid hack here to turn any 'mode' parameter back into hex
        # and probably print nicer than just the dict() representation
        self.info("actions planned: (%s)" % what, indent=RESOURCE_RESULT_INDENT)

    def on_provider_execute_command(self, resource, provider, command):
        """
        The provider ran a shell command.
        """
        # FIXME: logic like if provider.quiet() should exist like this, not down
        # further in the callbacks. The callbacks should always fire.
        if not provider.quiet():
            self.info("executing: (%s)" % command.cmd, indent=COMMAND_INDENT)

    def on_provider_execute_command_result(self, resource, provider, command, result):

        # the command result will always be non-fatal because otherwise we'll raise an error instead
        if result.fatal:
            self.info("> (%s) " % result, indent=COMMAND_RESULT_INDENT)
            self.failed.append(resource)
            self.FATAL()
        elif not provider.quiet():
            self.info("> (%s) " % result, indent=COMMAND_RESULT_INDENT)

    def on_command_echo(self, resource, provider, cmd, line):
        self.debug("| %s " % line.rstrip(), indent=COMMAND_ECHO_INDENT)

    def on_echo(self, resource, provider, msg):
        self.indent_echo(msg)

    def indent_echo(self, msg):
        msg = msg.splitlines()
        for line in msg:
            self.debug("| %s " % line.rstrip(), indent=COMMAND_ECHO_INDENT)
        

    def on_actions_apply_end(self, policy, resource, provider, actions, dry_run=False, handler=False):
        """
        We're done changing a resource.
        """

        planned = sorted([ str(x) for x in provider.actions_planned ])
        taken = sorted([ str(x) for x in provider.actions_taken ])

        if len(taken) > 0:
            self.changed.append(resource)
            if handler:
                self.changed_handlers.append(resource)
            else:
                self.changed_resources.append(resource)

        # self.debug("actions taken: (%s)" % list(taken), indent=RESOURCE_RESULT_INDENT)
        if (not dry_run) and (sorted(planned) != sorted(taken)):
            self.info(f"FATAL: actions planned ({planned}) do not equal actions taken ({taken})", indent=RESOURCE_RESULT_INDENT)
            self.FATAL()

    def on_result(self, policy, resource, provider, result, handler=False):
        if not result.fatal:
            if not provider.quiet():
                self.info("result: %s" % result, indent=RESOURCE_RESULT_INDENT)
            
            self.successful.append(resource)
            if not handler:
                self.successful_resources.append(resource)
            else:
                self.successful_handlers.append(resource)

        else:
            self.error("result: %s" % result, indent=RESOURCE_RESULT_INDENT)
            self.failed.append(resource)
            if not handler:
                self.failed_resources.append(resource)
            else:
                self.failed_handlers.append(resource)

            if not resource.ignore_errors:
                 self.FATAL()

    def on_skipped(self, policy, resource, condition, handler=False):
        self.info("skipped, condition: %s" % condition.describe(), indent=RESOURCE_RESULT_INDENT)
        self.skipped.append(resource)
        if handler:
            self.skipped_handlers.append(resource)
        else:
            self.skipped_resources.append(resource)

    def on_actions_handler_begin(self, policy, resource, provider):
        self.info("handling signal: %s" % resource.handles, indent=RESOURCE_RESULT_INDENT)
        self.handlers.append(resource)

    def on_signal_flagged(self, policy, resource, notify_name):
        """
        Indicate the resource wants to be triggering some handlers.
        """
        # FIXME: we should provide a way to complain about signals
        # that did not have a handler. Not in callback code, but somewhere
        self.info("signals: %s" % (notify_name), indent=RESOURCE_RESULT_INDENT)

    def info(self, msg, indent=0):
        self.msg(msg, indent=indent)

    def debug(self, msg, indent=0):
        self.msg(msg, indent=indent)

    def error(self, msg, indent=0):
        self.msg(msg, indent=indent)

    def msg(self, msg, indent):
        if msg == "":
            print("")
            return
        spc = INDENT * indent
        lines = msg.splitlines()
        for line in lines:
            print("%s%s" % (spc, line))

    def on_complete(self, policy):
        self.info("")
        self.summarize()

    def FATAL(self, exception=None):
        self.info("")
        self.summarize()
        sys.exit(1)
       

    
    

