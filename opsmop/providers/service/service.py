from opsmop.providers.provider import Provider

class Service(Provider):
    
    """
    Contains some fuzzy matching code all service instances should be able to use
    """

    def _is_started(self, status):
        if not status:
            return False
        return status in [ 'running', 'started' ]

    def _is_enabled(self, status):
        if not status:
            return False
        return status in [ 'running', 'started', 'stopped', 'enabled' ]

    def plan(self, facts, on_boot=True):

        status = self._get_status()

        if self._is_started(status):
            if not self.started:
                self.needs('stop')
        else:
            if self.started:
                self.needs('start')
            elif self.restarted:
                self.needs('restart')

        if on_boot:
            # this part of the planner can be switched off for services
            # that don't support it, allowing them to not fail when they
            # are only able to execute part of the plan
            if self._is_enabled(status):
                if not self.enabled:
                    self.needs('disable')
            else:
                if self.enabled:
                    self.needs('enable')
