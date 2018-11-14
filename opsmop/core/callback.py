# FIXME: this is moving in the right direction but still needs to get refactored a good bit

class BaseCallback(object):

    def set_context(self, context):
        self._context = context

    def context(self):
        return self._context

    def set_context(self, value):
        self._context = value
