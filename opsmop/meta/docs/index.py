
# Generate an RST page

import os

class Index(object):

    def __init__(self, records, dest_dir):

        self.dest_path = os.path.join(dest_dir, 'modules.rst')
        self.records = records

    
    def generate(self):
        self.fd = open(self.dest_path, "w")

        self.fd.write(".. _modules:\n")
        self.fd.write("\n")
        self.fd.write("OpsMop Module Index\n")
        self.fd.write("===================\n")   
        self.fd.write("\n")
        self.fd.write("Available modules by category:\n")
        
        categories = self.categories(self.records)

        for category in categories:
            self.fd.write("\n")
            self.fd.write(category.title() + "\n")
            clen = len(category)
            underscore = "-" * clen
            self.fd.write(underscore + "\n")
            self.fd.write("")

            for record in self.records_for_category(self.records, category):
                self.fd.write("* %s" % self.gen_rst_link(record))
            self.fd.write("\n")

        self.fd.close()
        print("written: %s" % self.dest_path)

    def categories(self, records):
        return sorted(set([ r.category for r in records ]))

    def records_for_category(self, records, category):
        return [ r for r in records if r.category == category ]

    def gen_rst_link(self, record):
        name = record.name
        return ":ref:`module_%s` - %s\n" % (record.name, record.purpose)

    