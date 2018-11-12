
# while DSL users can import anything they want, this makes some imports more friendly
# for shorter files for the most basic of site descriptions
# if you are writing your own modules you do not have to add them to this file to use them

# if someone knows a better way to do this please let me know :)

#import importlib
#__all__ = []
#def re_export(package, symbol):
#    m1 = importlib.import_module(package)
#    c1 = getattr(m1, symbol)
#    __all__.append(symbol)

from opsmop.core.policy import Policy as _Policy
from opsmop.core.roles import Roles as _Roles
from opsmop.core.role import Role as _Role
from opsmop.core.handlers import Handlers as _Handlers
from opsmop.core.resources import Resources as _Resources

from opsmop.conditions.condition import Condition as _Condition
from opsmop.conditions.all import All as _All
from opsmop.conditions.one import One as _One
from opsmop.conditions.equal import Equal as _Equal
from opsmop.conditions.less import Less as _Less
from opsmop.conditions.more import More as _More
from opsmop.conditions.var import V as _V
from opsmop.conditions.fact import F as _F
from opsmop.conditions.filetest import FileTest as _FileTest
from opsmop.conditions.choice import Choice as _Choice

from opsmop.types.file import File as _File
from opsmop.types.echo import Echo as _Echo
from opsmop.types.service import Service as _Service
from opsmop.types.package import Package as _Package
from opsmop.types.shell import Shell as _Shell
from opsmop.types.set import Set as _Set
from opsmop.types.stop import Stop as _Stop

# Core Resources
Policy = _Policy
Roles = _Roles
Role = _Role
Handlers = _Handlers
Resources = _Resources

# Conditions
Condition = _Condition
All = _All
One = _One
Equal = _Equal
FileTest = _FileTest
Less = _Less
More = _More
Choice = _Choice
V = _V
F = _F



# Types
File = _File
Service = _Service
Package = _Package
Echo = _Echo
Shell = _Shell
Set = _Set
Stop = _Stop


