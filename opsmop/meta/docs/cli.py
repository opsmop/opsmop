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


