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

import sys

from opsmop.meta.docs.generator import Generator

# automatic documentation generator
#
# converts files in the repo opsmop-demo (module_docs/*.py) into RST files 
# in docs/source/modules/*.rst in this repo and generates an the index in 
# docs/source/modules.rst.  These assets are then checked in and used
# to build the documentation website (make docs from repo root).

if __name__ == '__main__':

    examples_dir = sys.argv[1]
    dest_dir = sys.argv[2]
    
    Generator(examples_dir=examples_dir, dest_dir=dest_dir).go()
