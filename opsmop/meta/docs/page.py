import os

class Page(object):

    def __init__(self, record, dest_dir):

        self.dest_path = os.path.join(dest_dir, "module_%s.rst" % record.name)
        self.record = record

    
    def generate(self):
        pass