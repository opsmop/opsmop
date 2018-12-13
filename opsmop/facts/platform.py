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
import shutil

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
        """
        Loads OS names and versions. 
        """
        # patches welcome! feel free to update this for your distribution

        if os.path.exists("/etc/lsb-release"):
            # Debian/Ubuntu.
            data = open("/etc/lsb-release").read().splitlines()
            distribution = None
            release = None
            codename = None
            for line in data:
                if line.startswith("DISTRIB_ID"):
                    distribution = line.split("=")[-1].strip()
                elif line.startswith("DISTRIB_RELEASE"):
                    release = line.split("=")[-1].strip()
                elif line.startswith("DISTRIB_CODENAME"):
                    codename = line.split("=")[-1].strip()
            return dict(distribution=distribution, version=release, variant=codename)
        elif os.path.exists("/etc/redhat-release"):
            # RHEL/CentOS/Scientific Linux/Fedora
            data = open("/etc/redhat-release").read()
            tokens = data.split()
            for (i,t) in enumerate(tokens):
               if '.' in t:
                  break
            distribution = " ".join(tokens[0:i-1])
            variant = " ".join(tokens[i:-1])
            return dict(distribution=distribution, version=tokens[i], variant=variant)
        elif os.path.exists("/etc/system-release"):
            # Amazon Linux. Needs testing. May not be optimal for other distros.
            data = open("/etc/system-release").read().splitlines()
            distribution = None
            release = None
            rdate = None
            for line in data:
                if line.startswith("NAME"):
                    distribution = line.split("=")[-1].strip()
                elif line.startswith("VERSION"):
                    tokens = line.split(None, 2)
                    release = tokens[0]
                    rdate = tokens[1].replace("(","").replace(")","").strip()
            return dict(distribution=distribution, version=release, variant=rdate)
        else:
            if self.system() == "Darwin":
                return dict(distribution="Darwin", version=self.release(), variant=None)
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
        # patches welcome! feel free to update this for your distribution        
        distro = self.os_distribution()
        if distro == "Darwin":
            from opsmop.providers.package.brew import Brew
            return Brew
        elif distro == "Fedora":
            from opsmop.providers.package.dnf import Dnf
            return Dnf
        elif distro in ['CentOS Linux', 'Red Hat Linux', 'Amazon Linux', 'Scientific Linux']:
            # Amazon Linux, Scientific Linux, add yourselves here after testing
            # this will need some logic to decide when to use dnf
            from opsmop.providers.package.yum import Yum
            return Yum
        elif shutil.which("apt"):
            from opsmop.providers.package.apt import Apt
            return Apt
        return None

    def default_service_manager(self):
        # patches welcome! feel free to update this for your distribution        
        distro = self.os_distribution()
        if distro == "Darwin":
            from opsmop.providers.service.brew import Brew
            return Brew
        else:
            from opsmop.providers.service.systemd import Systemd
            return Systemd

    def default_user_manager(self):
        # patches welcome! feel free to update this for your distribution        
        distro = self.os_distribution()
        if distro != "Darwin":
            from opsmop.providers.user.useradd import UserAdd
            return UserAdd
        else:
            # someone may want to add this later, but skipping for now
            return None

    def default_group_manager(self):
        # patches welcome! feel free to update this for your distribution        
        distro = self.os_distribution()
        if distro != "Darwin":
            from opsmop.providers.group.groupadd import GroupAdd
            return GroupAdd
        else:
            return None

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
