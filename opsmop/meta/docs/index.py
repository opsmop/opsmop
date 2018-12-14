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

# Generate an RST page

import os


class Index(object):

    def __init__(self, records, dest_dir):

        self.dest_path = os.path.join(dest_dir, 'modules.rst')
        self.records = records

    
    def generate(self):
        self.fd = open(self.dest_path, "w")

        self.fd.write(".. image:: ../opsmop.png\n")
        self.fd.write("   :alt: OpsMop Logo\n\n")

        self.fd.write(".. _modules:\n")
        self.fd.write("\n")
        self.fd.write("OpsMop Module Index\n")
        self.fd.write("===================\n")   
        self.fd.write("\n")
        self.fd.write("Available modules by category:\n\n")
        
        categories = self.categories(self.records)

        for category in categories:

            self.fd.write("%s" % category.title())
            clen = len(category)
            self.fd.write("\n")
            self.fd.write("-" * clen)
            self.fd.write("\n")


            self.fd.write(".. list-table:: \n")
            self.fd.write("    :header-rows: 1\n\n")
            self.fd.write("    * - Name\n")
            self.fd.write("      - Purpose\n")
            for record in self.records_for_category(self.records, category):
                self.fd.write("    * - %s\n" % self.gen_rst_link(record))
                self.fd.write("      - %s\n" % record.purpose)

            self.fd.write("\n")
            self.fd.write("\n")

        
        self.fd.write("Something Missing ?\n")
        self.fd.write("-------------------\n")
        self.fd.write("\n")
        self.fd.write("No doubt there is.\n")
        self.fd.write("If you don't see what you want yet? Opsmop is very new and modules and capabilities are being added all the time!.\n")
        self.fd.write("Your needs matter to us. Think there should be a new module, a new parameter, or want to help build a new provider? You are welcome to stop by the :ref:`forum`.\n")
        self.fd.write("\n")

        self.fd.close()
        print("written: %s" % self.dest_path)

    def categories(self, records):
        return sorted(set([ r.category for r in records ]))

    def records_for_category(self, records, category):
        return [ r for r in records if r.category == category ]

    def gen_rst_link(self, record):
        return ":ref:`%s <module_%s>`" % (record.name.title().replace("_",""), record.name)
