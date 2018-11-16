from opsmop.meta.docs.exparser import Record
from opsmop.meta.docs.index import Index
from opsmop.meta.docs.page import Page

import glob
import os

class Generator(object):

    def __init__(self, examples_dir=None, dest_dir=None):
        self.examples_dir = examples_dir
        self.dest_dir = dest_dir

    def find_files(self):
        path = os.path.join(self.examples_dir, "*.py")
        files = glob.glob(path)
        return files

    def go(self):
        files = self.find_files()
        records = []
        for f in files:
            record = Record.from_file(f)
            records.append(record)

        print("==========================================================")
        for record in records:
            print("rendering page for record: %s with %s examples" % (record, len(record.examples)))
            Page(record, self.dest_dir).generate()
        print("rendering index for (%s) records" % len(records))
        Index(records, self.dest_dir).generate()
        print("done")
    

