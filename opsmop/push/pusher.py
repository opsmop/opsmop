class Pusher(object):

    def __init__(self, policies=None):
        self.policies = policies

    def check(self):
        print("check: %s", self.policies)

    def apply(self):
        print("apply: %s", self.policies)