.. image:: opsmop.png
   :alt: OpsMop Logo

.. _push:

Push Mode
---------


OpsMop's "Push Mode" works like local mode, but targets multiple remote systems simultaneously.

Push mode policies in OpsMop are just like Local policies (see :ref:`local`), and only require some very small extra 
functions to be implemented.

While OpsMop policy files written just for "local mode" do *NOT* contain enough information to be used
in push mode, any push-capable policy file *CAN* be used in local mode with *NO* changes. This is a free bonus, as sometimes you may want to develop
some automation locally as opposed to against remote systems.

What a push mode example looks like is best understood after first understanding the language in local mode, and then reading 
the `push_demo.py <https://github.com/opsmop/opsmop-demo/blob/master/content/push_demo.py>`_ example.

Please review this in another tab while reading the rest of the documentation.

.. _how_push_works:

How Things Work
===============

When in remote mode, it is helpful to think of remote communication, just as in local mode, as happening on a role by role basis.
For each role, the system will remotely connect to any hosts (or groups of hosts) referenced in that role, and tell them to start evaluating
that role.

This happens asynchronously: each host is trying to execute through the role as fast as it can, rather than task by task.
Along the way, various events occur and are sent back to the remote client, showing realtime status as configuration
occurs.  All hosts must finish before moving on to the next role.

If any host hits an error, the whole process stops with that role, and does not proceed to future roles.  

.. _push_cli:

Command Line Usage
==================

Similar to :ref:`local`, the opsmop command line for push mode is short::

    cd opsmop-demo/content
    python3 filename.py --check --push [--verbose]
    python3 filename.py --apply --push [--verbose]

Configuration is largely defined in the policy file.  There are other flags, but that's the minimum.

.. _push_role_methods:

Role Methods
============

Roles in OpsMop are described in :ref:`roles`, but with additional functions added to describe both which
hosts get contacted, and how, that are exclusively used with the '--push' CLI flag.

There are a few more we'll get to later, but let's review the most important ones. Note that not all of them
are always required, so don't get overwhelmed at first:

.. code-block: python

    inventory = TomlInventory("inventory/inventory.toml")

    class DemoRole(Role):

        def inventory(self):
            # required! we'll explain this shortly
            return inventory.filter(groups='webservers*')

        def ssh_as(self):
            # optional.
            # specifies SSH username and password.  If no password, will try an SSH key.
            # if you MUST use a password, maybe load it from a file.
            return ('opsmop', None)

        def sudo(self):
            # optional. 
            # whether to sudo after logging in. Defaults to False.
            return True

        def sudo_as(self):
            # optional. 
            # username and optionally a password for the sudo account. If not set, tries root / no-password.
            return ('root', None)

        def check_host_keys(self):
            # whether to check host keys, the default is True - if dealing with frequently changing systems, False may be better.
            # there is no system to auto-add host keys (yet), so you would have to use ssh-keyscan and add them.
            return False

        def main(self):
            # this isn't new
            File("/tmp/test.txt", from_content="I'm making a note here, huge success.")


.. note:

    If you need a review of basic language features, see :ref:`language` and :ref:`advanced`.  All the language features you
    learned in those chapters work together with this new information.

.. note:

    This may seem like a lot of methods to define for each role, but remember that OpsMop is Python, and you can define
    a BaseRole and then subclass from it to keep your roles short and organized!

.. note::

   In all computer systems, not just OpsMop, SSH connection with keys to untrusted hosts can be insecure, 
   because that host can read your password. Wherever possible, you should connect by SSH key.

.. note::

    Usage of ssh-agent with  SSH keys is highly recommended for ease of automation, and the integrated SSH key management
    features of `Vespene <http://docs.vespene.io>` pair well with OpsMop push mode.

.. _sudo_notes:

Sudo
====

It is worth noting that the sudo operations that happen above happen only once per role.  SSH connections, however, are reused
between subsequent roles. 

The most common use of sudo is to log in as a normal account and then sudo to root, rather than allowing SSH to the root account.
From root, it is easy to trivially execute sudo to less priveledged accounts, if needed, but this is not done with the 'sudo_as' 
methods, you would simply just specify 'sudo' in front of any shell commands.

Or, to put it another way, we expect 'sudo_as' to be used for priveledge escalation most of the time.  This is why you can
leave the 'sudo_as' undefined if you want, and it will just try root and no-password.
         
.. _push_inventory:

Inventory
=========

Push mode requires an inventory to decide what hosts to target.  Inventory can also attach variables
to each host (for use in :ref:`templates` or conditionals), and there are certain special
variables that can influence how the push mode operates.

Inventory objects can be filtered, as shown above and in 'push_demo.py', by specifying a `fnmatch <https://docs.python.org/3/library/fnmatch.html>`_ pattern.
For instance, an inventory can be carved down to a particular list of groups and/or hosts.

As detailed above, inventory is specified on each role, like this:

.. code-block:: python

    def inventory(self):
        return inventory.filter(groups='webservers')

That's an explicit group name.  We could also match groups starting with a pattern:

.. code-block:: python

    def inventory(self):
        return inventory.filter(groups='dc*')

The inventory class also allow filtering by host names, though usually you should just use groups:

.. code-block:: python

    def inventory(self):
        return inventory.filter(hosts='*.dc.example.com')

And, finally, the inventory filtering supports multiple patterns:

.. code-block:: python

    def inventory(self):
        return inventory.filter(groups=['webservers','dbservers'])

Recall that OpsMop is pure python, so as long as you return an inventory object from this method, you can do whatever
you want with it, including subclassing inventory.

.. _inventory_limits:

Inventory Limits on the Command Line
====================================
       
The inventory groups used can be further limited on the command line as follows::

    python3 push_demo.py --push --apply --limit-groups 'rack1'
    python3 push_demo.py --push --apply --limit-hosts 'foo.example.com'

This way, it's easy to write generic automation scripts that can target arbitrary inventory, without having to change the policy files.
It is of course important to remember that, once again, OpsMop is pure python, and you could also do all this dynamically from within the policy file.

.. _toml_inventory:

Toml Inventory
==============

An easy method of keeping inventory in source code is the TOML Inventory, best demonstrated 
by `inventory.toml <https://github.com/opsmop/opsmop-demo/blob/master/content/inventory/inventory.toml>`_.

Variables can be assigned at either host or group level.

.. _other_inventory:

Other Inventory Types
=====================

Additional inventory types classes, particularly for cloud providers, would make excellent contributions to OpsMop.  If you are interested in 
adding one, stop by `talk.msphere.io <talk.msphere.io>`_.

This will likely include cloud providers, querying inventory from configurations, and group membership from tags.  Once complete, setup and usage
will be documented here.

.. _magic_inventory_variables:

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
    * opsmop_via - name of the parent host (see :ref:`connection_trees`)
    * opsmop_python_path - the path to python 3 on the remote system (defaults to /usr/bin/python3)

Variables can be set on  hosts or groups.  Setting them on groups is usually preferred where possible to reduce duplication, though obviously
this doesn't make sense for 'opsmop_host'.

.. _connection_trees:

Connection Trees
================

Connection trees are an optional feature supported by the underlying library "mitogen" that we use for SSH communications 
(help is needed testing them!).  

OpsMop (via mitogen) can SSH-connect through multiple-layers of intermediate hosts, in a fan-out architecture.

Here is an Example using the TOML inventory, to make it easier to understand the structure:

.. code-block: toml

    [groups.bastions.hosts]
    "bastion.example.com" = ""

    [groups.rack1.hosts]
    "rack1-top.example.com" = "opsmop_via=bastion.example.com"
    "rack1-101.example.com" = ""
    "rack1-102.example.com" = ""

    [groups.rack2.hosts]
    "rack2-top.example.com" = "opsmop_via=bastion.example.com"
    "rack2-201.example.com" = ""
    "rack2-202.example.com" = ""

    [groups.rack1.vars]
    opsmop_via = "rack1-top.example.com"

    [groups.rack2.vars]
    opsmop_via = "rack2-top.example.com"

    [groups.fooapp.hosts]
    "rack1-101.example.com" = ""
    "rack2-202.example.com" = ""

    [groups.barapp.hosts]
    "rack2-102.example.com" = ""

.. code-block: python

    class FooApp(Role):

        def inventory(self):
            return inventory.filter(groups='fooapp')
        # ...

.. _push_fileserver:

Understanding the FileServer
============================

OpsMop provides files to servers that need them through the SSHd channel, also courtesy of the mitogen library.

To prevent a rogue host from requesting files that it should not have access to, the file serving features of OpsMop in push mode
are 'opt-in'.

By default, it is possible to reference any paths relative to the main policy file, as featured in 'push_demo.py', and those
files "just work".

To access other paths, a method can be added to the change what paths are served for that role:

.. code-block: python

    class FooRole(Role):

        def allow_fileserving_paths(self):
            return [ '.', '/opt/files' ]

        def main(self):
            File("/opt/destination/large.file", from_file="/opt/files/large.file")

"." in this case, always means the path of the policy file being executed on the command line.  If any other paths are given,
they should be referenced as absolute paths by any resources that use them, as shown above.  If an 'allow_fileserving_paths'
method is not found on the Role, there is also an opportunity to override the default path ('.') by defining a method on the Policy
class. 

The basic takeaway here is that each Role has fine grained control over what files may be served up.  


When the paths are added to the role, checksumming is performed to avoid transferring any files that do not need to be transferred.

To avoid excessive checksumming, and also for security reasons, a set of patterns to be included and excluded from FileServing
is available on the policy object.  The defaults are largely sensible for most applications:

.. code-block: python

    class YourPolicy(Policy):

        def allow_fileserving_patterns(self):
            return [ '*' ]

        def deny_fileserving_patterns(self):
            return [ '*.py', "*__pycache__*", '*.pyo', '*.pyc', '.git', '.bak', '.swp' ]

You may ask why this is important.  Part of the reason is we don't want to allow a rogue host SSHd or Python to request files it should
not have access to, or to allow accidental errors from users sending sensitive files to untrusted hosts.  The other part is we want to avoid
calculating checksums for files we are unlikely to serve up.

.. _push_advanced_tricks:

Advanced Tricks: Rolling Updates And More
=========================================

While less commonly needed in cloud-enabled scenarios where "blue-green" deployments are common, the scenario of rolling updates
is a good one to use to describe many of the advanced features of OpsMop push mode.  These features are not, however, limited to
rolling update capabilities.

In a rolling update, suppose we have 100 hosts connected to a physical load balancer.  What we want to do is contact 10 hosts
at a time, and before updating them, take them out of a load balanced pool.  If they succeed with their updates, we want to put
them back into that load balanced pool.

The OpsMop role might look like this:

.. code-block: python

    class RollingWebServerUpdate(Role):

        def inventory(self):
            # ...

        def set_resources(self):
            # ...

        def set_handlers(self):
            # ....

        def should_contact(self, host):
            # can decide to ignore specific hosts
            return True

        def ssh_as(self):
            return (UserDefaults.ssh_username(), None) # use keys

        def sudo_as(self):
            # if no sudo password is required, just say "None"
            return (UserDefaults.sudo_username(), UserDefaults.sudo_password())

        def sudo(self):
            # yes, we should sudo
            return True

        def serial(self):
            # this many hosts execute at once
            return 10

        def before_connect(self, host):
            # this runs on the control machine
            subprocess.check_rc("unbalance.sh %s" % host.hostname())

        def main(self):
            # do meaningful work here

        def after_connect(self, host):
            # this runs on the control machine
            subprocess.check_rc("balance.sh %s" % host.hostname())


As you can see, there are a lot of details to this example, but full control is provided.  Interaction with any piece of hardware, database, or system - including
waiting on external locks, is completely possible *without* needing to rely on extra modules.

While this type of workflow mostly makes sense for a rolling updates with hardware load balancers, the "before_connect" and "after_connect" hooks are completely generic
and can be used for any purpose.

Similarly, the serial control affects how many hosts are going to be processed at any one time, and can be useful when controlling load on a package updates. For instance, if you
had 3000 hosts, it might be a bad idea to let them all hit your package mirror at once.

The serial control also provides a nice failsafe - if there are errors in a serial batch, it can prevent the rest of the hosts from being taken out by a failure during the policy
application.  There is *always* a default value for "serial" in OpsMop, but the default is currently hard coded to do 80 roles a time.  This can easily be made configurable
in future releases.

.. _push_tuning:

Tuning
======

The SSH implementation is already very fast, but there are a few things you can do to boost performance.

Your opsmop providers likely have python library dependencies.  While opsmop does not require
that you install these dependencies on managed nodes, if you install them, this will
greatly speed up execution time.

These include python packages: jinja2, toml, dill, colorama, and PyYAML.

If not installed, the module code for these are copied over once per each push execution.

.. _push_status:

Current Status
==============

Push mode is still a little new, and can use help testing in all manner of configurations, including in high-
performance, high-host-count, and high-latency scenarios.  However, most features are already implemented
and this is completely usable today.

1. SELinux (enforcing) support is not operational yet and is waiting on enhancements in mitogen. You should
be able to switch selinux to permissive mode.  Non-SELinux distributions (Debian, Ubuntu, Arch, etc) 
are of course not effected.

2. Connecting to new hosts (but not the actual management operations) are conducted in a threadpool with a default of 16 threaded workers. If you have a large
number of hosts there may be some lag for the very first time they are contacted that will not occur in subsequent roles. 
A future forks flag like "-j4" should allow this to use additional CPUs by dividing the list of hosts up between processors.

Logging
=======

Sometimes it is easier to understand a problem with a configuration policy when viewing the remote log from the perspective of a local
deploy.

To do this, simply login to the remote system and cat ~/.opsmop/opsmop.log

The output will contain the exact output as if the configuration was run locally, with timestamps.  The file is automatically logrotated
so you do not need to worry about it growing too large.

This path should be configurable in the future.

Credits
=======

Much of the support for push mode in OpsMop comes from the libraries underpinning the implementation, and we would be remiss to not give them
due credit for makings these features much easier to implement.

OpsMop SSH features, including sudo support, file transfer, dependency transfers, remote error handling, and multi-tier connections 
are all powered by `mitogen <https://mitogen.readthedocs.io/en/latest/>`_.

Additionally, heavy use is made of `dill <https://pypi.org/project/dill/>`_ for serialization of python objects.

The asynchronous connections benefit strongly from `concurrent futures <https://docs.python.org/3/library/concurrent.futures.html>`_, a great
improvement on the multiprocessing layer.

