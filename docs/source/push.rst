.. image:: opsmop.png
   :alt: OpsMop Logo

.. _push:

Push Mode
---------

OpsMop push mode is very similar to :ref:`local`, but operates on multiple hosts via SSH.

This is best understood while reviewing the `push_demo.py <https://github.com/opsmop/opsmop-demo/blob/master/content/push_demo.py>`_ example.

Command Line Usage
==================

Similar to :ref:`local, the opsmop command line for push mode is very simple::

    opsmop-push --check filename.py
    opsmop-push --apply filename.py

Configuration is largely defined in the policy file.  Additional CLI flags may be added over time.

Role Methods
==============

The following new methods are useful on each *Role* object in OpsMop when invoked in pull mode:

.. code-block: python

    inventory = TomlInventory("inventory/inventory.toml")

    class DemoRole(Role):

        def inventory(self):
            return inventory.filter(groups='webservers*')

        def ssh_as(self):
            # username and optionally a password
            return ('opsmop', None)

        def sudo(self):
            # whether to sudo
            return True

        def sudo_as(self):
            # username and optionally a password
            return ('root', None)

        def check_host_keys(self):
            # the default is True
            return False

This is in addition the the usual parts of the role, which are used in both local and push modes:

.. code-block: python

    def set_resources(self):
        # ...

    def set_handlers(self):
        # ...

    def set_variables(self):
        # ...

    def should_process_when(self):
        # ...

    def pre(self):
        # ...

    def post(self):
        # ...

If you need a review of basic language features, see :ref:`language` and :ref:`advanced`.

.. note::

   In all computer systems, not just OpsMop, SSH connection with keys to untrusted hosts can be insecure, 
   because that host can read your password. Wherever possible, you should connect by SSH key.

.. note::

    Usage of ssh-agent with  SSH keys is highly recommended for ease of automation, and the integrated SSH key management
    features of `Vespene <http://docs.vespene.io>` pair well with OpsMop push mode.


Defaults
========

For values not specified on the role object, defaults are first looked for in ~/.opsmop/defaults.toml.  If that file does
not exist, defaults are looked for in /etc/opsmop/defaults.toml.

The file has the following format::

    [ssh]
    username = "mpdehaan"
    # password = "1234"
    # check_host_keys = "ignore"

    [sudo]
    username = "root"
    # password = "letmein1234"

These values are IGNORED if returned as "None" in the "sudo_as" or "connect_as" methods on the *Role* object.
         
Inventory
=========

Pull mode requires an inventory to decide what hosts to target.  Inventory can also attach variables
to each host (for use in :ref:`templates` or :ref:`conditionals`), and there are certain special
variables that can influence how the push mode operates.

Inventory objects can be filtered, as shown above, by specifying a `fnmatch <https://docs.python.org/3/library/fnmatch.html>`_ pattern.
For instance, an inventory can be carved down to a particular list of groups and/or hosts.

Toml Inventory
==============

An easy method of keeping inventory in source code is the TOML Inventory, best demonstrated 
by `inventory.toml <https://github.com/opsmop/opsmop-demo/blob/master/content/inventory/inventory.toml>`.

Variables can be assigned at either host or group level.

Other Inventory Types
=====================

Additional inventory types classes, particularly for cloud providers, would make excellent contributions to OpsMop.  If you are interested in 
adding one, stop by `talk.msphere.io <talk.msphere.io>`.

Magic Inventory Variables
=========================

Certain variables, when assigned in inventory, can be used to specify default values for SSH and Sudo behavior, and are used
*INSTEAD* of the values in default.toml files if they exist.

These variables are usable regardless of inventory source::

    * opsmop_host - the address to connect to
    * opsmop_ssh_username - the SSH username
    * opsmop_ssh_password - the SSH password
    * opsmop_sudo_username - the sudo username
    * opsmop_sudo_password - the sudo password

Current State
=============

* Push mode is an early alpha
* Work needs to be done to enable file transfer
* SELinux may not be operational

Credits
=======

OpsMop SSH features are powered by `mitogen <https://mitogen.readthedocs.io/en/latest/>`.

Not all of mitogen features are exposed at this point (such as multi-layer routing) and more features can be surfaced 
in the future.
