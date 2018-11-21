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

import os

class Example(object):

    def __init__(self): 
        # things we'll figure out as we scan an example
        self.name = ""
        self.see_files = []
        self.description = []
        self.code = []

class Record(object):

    def __init__(self):
        # things which we'll figure out as we scan the example
        self.name = ""
        self.purpose = ""
        self.provider_names = []
        self.related_modules = []
        self.category = ""
        self.description = []
        self.examples = []
        self.current_example = Example()
        self.phase = 'module'
        self.count = 0
    
    def set_phase(self, phase):
        self.phase = phase

        print("---------------------------------------------------------")
        print("%s phase | %s" % (self.count, self.phase))
        print("---------------------------------------------------------")

    @classmethod
    def from_file(cls, filename):
        r = cls()
        r.name = os.path.basename(filename).replace(".py","")
        print("=========================================================")
        print("%s M     | %s" % ('0', r.name))
        data = open(filename).read().splitlines()
        for line in data:
            if not r.handle_line(line):
                break
        return r

    def load_command(self, line):
        if "DESCRIPTION" in line or '----' in line or '====' in line:
            pass
        elif not ":"  in line:
            # commands must contain a colon unless they are blocks or DESCRIPTION starters
            return (False, None, None)

        if not line.startswith("#"):
            # commands must be in comments
            return (False, None, None)
        if ":" in line:
            tokens = line.split(":")
            if tokens[0].upper() != tokens[0]:
                # commands must be in all caps. This is done
                # so we don't get confused by colons in URLs and so on.
                print("REJECT: %s" % tokens[0])
                return (False, None, None)
        # at this point we are sure it is a command
        if '#------------' in line.replace(" ",""):
            return (True, 'start_block', None)
        if '#============' in line.replace(" ",""):
            return (True, 'end_block', None)
        # throw away the leading comment
        line = line.replace("#","",1).strip()
        if line.startswith("DESCRIPTION"):
            return (True, 'description', None)
        tokens = line.split(':', 1)
        command = tokens[0].replace("#","").strip().lower()
        rest = tokens[1].strip()
        return (True, command, rest)


    def handle_line(self, line):
        self.count = self.count + 1

        (is_command, command, rest) = self.load_command(line)
        print("%s line  | %s" % (self.count, line))

        #if command == 'policy':
        #    return False

        if is_command:
            #if command not in [ 'start_block', 'end_block' ]:
            #    print("keyword: %s => %s" % (command, rest))
            self.handle_command(command, rest)
            return True

        #print("PHASE=%s" % self.phase)
        #print("LINE=%s" % line)

        if self.phase == 'module':
            if not line.startswith("#") or line.replace("#","").strip():
                raise Exception("the module phase should be all commands")
        
        elif self.phase == 'description':
            # module description lines must be comments
            self.handle_module_description(line)

        elif self.phase == 'example':
            if not line.startswith("#") or line.replace("#","").strip():
                raise Exception("the example phase should be all commands")
        
        elif self.phase == 'example_description':
            self.handle_example_description(self.current_example, line)

        elif self.phase == 'example_code':
            self.handle_example_code(self.current_example, line)

        elif self.phase == 'limbo':
            #print("ignoring line while in limbo: %s" % line)
            pass

        elif self.phase == 'done':
            #print("ignoring line while done: %s" % line)
            pass

        else:
            raise Exception("unknown phase: %s" % self.phase)

        return True # continue

    def handle_command(self, command, rest):
        #print("<PHASE: %s, COMMAND: %s, REST: %s>" % (self.phase, command, rest))

        if self.phase == 'done':
            return False

        if self.phase == 'module':
            # from module mode the only state transition is into module_description mode
            # when we find the description command
            if command not in ['start_block', 'end_block']:
                print("%s set   | %-20s | %s" % (self.count, command, rest))
            if command == 'module':
                pass
            elif command == 'start_block':
                pass
            elif command == 'category':
                self.category = rest
            elif command == 'purpose':
                self.purpose = rest
            elif command == 'related':
                self.related_modules = [ x.strip() for x in rest.split(",") ]
            elif command == 'providers':
                self.providers = [ x.strip() for x in rest.split(",") ]
            elif command == 'fyi':
                pass
            elif command == 'description':
                print("---------------------------------------------------------")
                self.set_phase('description')
            elif command == 'end_block':
                raise Exception("unexpected end block without description")
            else:
                raise Exception("unknown command: %s" % command)

        elif self.phase == 'description':
            # in description phase end block moves us into limbo until we find
            # another example start block
            if command == 'end_block':
                self.set_phase('limbo')
            else:
                raise Exception("invalid command: %s" % command)

        elif self.phase == 'limbo':
            # in limbo, seeing a start block moves us into example phase
            if command == 'start_block':
                self.set_phase('example')
            else:
                raise Exception("invalid command: %s" % command)

        elif self.phase == 'example':
            # in example phase we can only move into example description phase
            # by hitting the description command
            if command == 'example':
                print("---------------------------------------------------------")
                print("%s exmp  | %s" % (self.count, rest))
                print("---------------------------------------------------------")

                self.current_example.name = rest
            elif command == 'setup':
                self.set_phase('done')
            elif command == 'description':
                print("MOV!")
                self.set_phase('example_description')
            elif command == 'see_files' or command == 'see_file':
                self.current_example.see_files = [ x.strip() for x in rest.split(",")]
            else:
                raise Exception("unknown command: %s" % command)

        elif self.phase == 'example_description':
            # in example description phase we can only move into example code phase
            # by hitting an end block
            if command == 'end_block':
                print("-------")
                self.set_phase('example_code')
            else:
                raise Exception("unknown command: %s" % command)

        elif self.phase == 'example_code':
            # in example code phase we can only move back into example phase by 
            # hitting a start block
            if command == 'start_block':
                self.examples.append(self.current_example)
                self.current_example = Example()
                self.set_phase('example')
            else:
                raise Exception("unknown command: %s" % command)

        elif self.phase == 'done':
            return False
    
        else:
            raise Exception("unknown phase: %s" % self.phase)

    def handle_example_description(self, example, line):
        # could be a comment or the code example, we want to keep both
        if line.startswith("#"):
            line = line.replace("#","")
            line = line.strip()
            print("%s desc  | %s" %  (self.count, line))
            example.description.append(line)

    def handle_example_code(self, example, line):
        line = line.rstrip()
        example.code.append(line)
        print("%s code  | %s" % (self.count, line))


    def handle_module_description(self, line):
        if line.startswith("#"):
            line = line.replace("#","")
            line = line.strip()
            if line:
                print("%s mdesc | %s" % (self.count, line))
                self.description.append(line)
