from opsmop.providers.package.package import Package

TIMEOUT = 60
VERSION_CHECK = "brew ls --versions {name} | cut -f2 -d ' '"
INSTALL = "brew install {name}"
UPGRADE = "brew update {name}"
UNINSTALL = "brew uninstall {name}"

class Brew(Package):

    """
    Manages homebrew packages
    """
    
    def _get_version(self):
        version_check = VERSION_CHECK.format(name=self.name)
        return self.test(version_check)

    def get_default_timeout(self):
        return TIMEOUT

    def plan(self):
        super().plan()

    def apply(self):
        which = None
        if self.should('install'):
            self.do('install')
            which = INSTALL.format(name=self.name)
        elif self.should('upgrade'):
            self.do('upgrade')
            which = UPGRADE.format(name=self.name)
        elif self.should('remove'):
            self.do('remove')
            which = UNINSTALL.format(name=self.name)

        if which:
            return self.run(which)
        return self.ok()
        

