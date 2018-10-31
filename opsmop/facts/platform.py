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

import platform
import os

from opsmop.core.common import memoize
from opsmop.facts.facts import Facts

# TODO: there are a LOT of facts to add yet!  We are just starting out
# contributions are very welcome

class PlatformFacts(Facts):
    
    """
    As this evolves, facts can be dynamically injected into this base class based on platform, allowing a subclass
    for things like LinuxFacts. When this happens, we can have a "facts/" package.
    """

    @memoize
    def system(self):
        """ This returns strings like "Linux" and is generally not exceptionally useful. """
        return platform.system()

    @memoize
    def release(self):
        return platform.release()

    @memoize
    def version(self):
        """ On Linux, this returns the kernel version """
        return platform.version()

    @memoize
    def os_distribution_info(self):
        # feel free to add your distribution here
        if os.path.exists("/etc/redhat-release"):
            data = open("/etc/redhat-release").read()
            tokens = data.split()
            for (i,t) in enumerate(tokens):
               if '.' in t:
                  break
            distribution = " ".join(tokens[0:i-1])
            variant = " ".join(tokens[i:-1])
            return dict(distribution=distribution, version=tokens[i], variant=variant)
        return None

    @memoize
    def os_distribution(self):
        """ returns a string like 'CentOS Linux' """
        info = self.os_distribution_info()
        if info is None:
            return None
        return info['distribution']

    @memoize 
    def os_version_string(self):
        """ This returns the OS version such as X.Y.Z """
        info = self.os_distribution_info()
        if info is None:
            return None
        return info['version']

    @memoize
    def os_version_number(self):
        """ Returns an floating point version like 7.2, ignoring maintaince/build numbers """
        info = self.os_distribution_info()
        if info is None:
            return 0
        tokens = info['version'].split('.')
        major_minor = "%s.%s" % (tokens[0], tokens[1])
        return float(major_minor) 

    def default_package_manager(self):
        # TODO: this will return based on platform
        from opsmop.providers.package.brew import Brew
        return Brew

    def default_service_manager(self):
        # TODO: this will return based on platform
        from opsmop.providers.service.brew import Brew
        return Brew

    def constants(self):
        """
        This returns all facts that do not take parameters .
        Mostly for the DebugFacts() implementation
        """
        return dict(
            system = self.system(),
            release = self.release(),
            version = self.version(),
            default_package_manager = self.default_package_manager(),
            default_service_manager = self.default_service_manager(),
            os_distribution = self.os_distribution(),
            os_version_string = self.os_version_string(),
            os_version_number = self.os_version_number()
        )

    def invalidate(self):
        pass

Platform = PlatformFacts()

if __name__ == "__main__":
    print(Platform.constants())
