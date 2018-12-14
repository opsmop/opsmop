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

import glob
import os

from opsmop.meta.docs.exparser import Record
from opsmop.meta.docs.index import Index
from opsmop.meta.docs.page import Page


class Generator(object):

    def __init__(self, examples_dir=None, dest_dir=None):
        self.examples_dir = examples_dir
        self.dest_dir = dest_dir

    def find_files(self):
        path = os.path.join(self.examples_dir, "*.py")
        return glob.glob(path)

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
