
class Context(object):

    def __init__(self, callbacks=None):

        assert type(callbacks) == list
        self._callbacks = callbacks

    def _run_callbacks(self, cb_method, *args):
        """ 
        Run a named callback method against all attached callback classes, in order.
        """
        for c in self._callbacks:
            c.set_context(self)
            attr = getattr(c, cb_method)
            attr(*args)

    def on_apply(self, provider):
        self._run_callbacks('on_apply', provider)

    def on_finished(self, value):
        self._run_callbacks('on_finished')

    def on_echo(self, value):
        self._run_callbacks('on_echo', value)

    def on_plan(self, provider):
        self._run_callbacks('on_plan', provider)

    def on_role(self, role):
        self._run_callbacks('on_role', role)

    def on_command_echo(self, value):
        self._run_callbacks('on_command_echo', value)

    def on_execute_command(self, value):
        self._run_callbacks('on_execute_command', value)

    def on_resource(self, resource, is_handler):
        self._run_callbacks('on_resource', resource, is_handler)

    def on_command_result(self, value):
        self._run_callbacks('on_command_result', value)

    def on_planned_actions(self, provider, actions_planned):
        self._run_callbacks('on_planned_actions', provider, actions_planned)

    def on_taken_actions(self, provider, actions_taken):
        self._run_callbacks('on_taken_actions', provider, actions_taken)

    def on_result(self, result):
        self._run_callbacks('on_result', result)
        if result.fatal:
            self._run_callbacks('on_fatal', result)

    def on_skipped(self, value):
        self._run_callbacks('on_skipped', value)

    def on_flagged(self, value):
        self._run_callbacks('on_flagged', value)

    def on_complete(self, value):
        self._run_callbacks('on_complete', value)

    def on_all_policies_complete(self):
        self._run_callbacks('on_all_policies_complete')

    def on_conditions(self, value):
        self._run_callbacks('on_conditions', value)

    def on_update_variables(self, variables):
        self._run_callbacks('on_update_variables', variables)

    def on_evaluation_failed(self, expr):
        self._run_callbacks('on_evaluation_failed', expr)