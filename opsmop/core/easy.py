
# while DSL users can import anything they want, this makes some imports more friendly
# for shorter files for the most basic of site descriptions
# if you are writing your own modules you do not have to add them to this file to use them

# core
from opsmop.core.policy import Policy
from opsmop.core.roles import Roles
from opsmop.core.role import Role
from opsmop.core.resources import Resources
from opsmop.core.handlers import Handlers
from opsmop.facts.facts import Facts

from opsmop.lookups.eval import Eval 
from opsmop.lookups.template import T

# types
from opsmop.types.file import File
from opsmop.types.directory import Directory
from opsmop.types.service import Service
from opsmop.types.package import Package
from opsmop.types.shell import Shell
from opsmop.types.echo import Echo
from opsmop.types.set import Set
from opsmop.types.stop import Stop
from opsmop.types.asserts import Asserts
from opsmop.types.debug import Debug
from opsmop.types.debug_facts import DebugFacts

__all__ = [
    'Policy', 'Roles', 'Role', 'Resources', 'Handlers', 'Eval', 'T', 'Facts',
    'File', 'Directory', 'Echo', 'Service', 'Package', 'Shell', 'Set', 'Stop', 'Asserts', 'Debug', 'DebugFacts'
]