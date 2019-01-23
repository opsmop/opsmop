.. image:: opsmop.png
   :alt: OpsMop Logo

.. _advanced:

Language Part 2
---------------

Once you have covered the basics of the language in :ref:`language`, there are many more
additional language features you may be interested in.

We say these are 'advanced' features not because they are complicated, but just because they
are optional.  These are the features that you should learn second, or maybe third, after
trying out a few modules.

As we have mentioned, the use of the declarative module system in OpsMop is 100% optional.
You can easily just use OpsMop as a layer to call remote python RPC functions, and you can also intermix
raw imperative python with the declarative modules.

Many simple configurations in OpsMop may simply use modules like
:ref:`module_service`, :ref:`module_package`, and :ref:`module_file`, and 
will not need many modules, but they are worth exploring.

It is also important OpsMop encourages random-access learning.


The language examples below will refer to many modules detailed further in the :ref:`modules` section, so 
feel free to jump back and forth. The best way to understand these features is to consult
the `opsmop-demo <https://github.com/opsmop/opsmop-demo>`_ repo on GitHub, and also as you 
read through :ref:`modules`, you will see some of these features used in the examples in context.

Many of the examples are contrived and don't deploy real applications, but are constructed to teach 
lessons about things such as :ref:`var_scoping`.  Real OpsMop policies
for deploying an application stack would be a bit longer and would use a larger mixture of modules in concert.

By studying these arbitrary examples though, you can quickly experiment and try to put
them together in your own :ref:`policy` configurations.

OpsMop does not believe you should need an extremely large library of example configurations, we want you to learn
the tool and be able to easily construct your own.

.. _method:

Module Provider Selection
=========================

We've discussed module types a bit already.

When we talk about modules like "File()", "Service()", or "Package()" in OpsMop, we call them resources,
but really resources come in two parts - Types and Providers. 

Often, :ref:`types` may be coded to have only one provider implementation.  Other modules may choose a default based
on the operating sysstem. As an example, the File() resource has only one implementation but there will be
many different implementations for Package().

Providers are the implementation code that make system changes as expressed in a Type.  The Type just defines
the request.

To install a package using the default *Provider*, we don't have to do anything special:

.. code-block:: python

    def main(self):
        Package(name="cowsay") # install cowsay if not installed

However, the default type is not always the one you will want to use.  For instance, the default
Package provider on Ubuntu would be "apt", and on CentOS 7 it would be "yum", but what if we wanted
to install a package from Python's pip?

To specify or force a specific provider:

.. code-block:: python
    
    def main(self):
        Package(name="pygments", method="pip")

NOTE that at this point in OpsMop's development, we have a lot of providers to add for packages yet.
This makes a great point of contribution, so if you are interested, see the :ref:`community` section.

Ok, so that's how to pick a stock provider that the type is already coded to know exists as an option.

It's also possible to use a provider that OpsMop doesn't ship with, perhaps one that you wrote for
some of your own internal services:

.. code-block:: python

    def main(self):
        Package(name="cowsay", method="your.custom.provider.spork")

Expressing that full path for the provider name is verbose (and subject to typos), so it helps to save those strings to a python constant
to improve readability.

.. code-block:: python
    
    Package(name="cowsay", method=SPORK)

.. note:

    OpsMop is new so providers will be growing rapidly for modules.  These are a great
    first area for contributions if you have needs for one.  See :ref:`development`.

.. note:

    It is deceptive to assume a package name is the same on all platforms.  Conditionals and various
    other systems allow solutions, but in the most common cases, your site content will just need
    to code for the platform you use.  While multi-platform content is interesting, if you don't need
    it, don't worry about it.

.. _var_scoping:

Variable Scoping
================

This section talks about how variables win out over one another, when variables are defined at multiple levels.

OpsMop uses variables in both templates (like :ref:`module_file` or :ref:`module_echo`) and conditionals.

In the opsmop-demo repository, `var_scoping.py <https://github.com/opsmop/opsmop-demo/blob/master/content/var_scoping.py>`_ demonstrates
the various variable scopes in OpsMop. 

In the following list, the LAST variable listed wins out.

1. Any variables defined in inventory on a group (:ref:`push` only)
2. Any variables defined in inventory on a host (:ref:`push` only)
3. Any variables defined on the resource itself, such as a parameter passed into a role or policy object, including those defined
   inside the 'set_variables' function.
4. Any variables in local python scope inside the main function
5. Any variables sent to --extra-vars (see :ref:`extra_vars`)

If you ever need to access a variable inside a function (not a template), you can do this, *regardless* of the scope in which it is defined,
and you are guaranteed to always get the right value:

.. _code-block: python

    def main(self):
        if self.vars.x > 2:
           print(self.vars.x)
           
The GitHub example demo linked above is the best way to see these concepts linked together in practice.

.. _eval:

Conditions
==========

Conditions in OpsMop are just standard Python statements.  Conditions that are configuration related may hinge of :ref:`facts`,
which are pieces of information OpsMop can return about the target system.

.. code-block:: python

    def main(self):
        if Platform.system() != "Darwin":
            return
        Shell("reboot")

As listed above in :ref:`var_scoping`, usage of "self.vars.x" can be used to access a variable, even if it is not defined in local
scope.

.. _registration:

Registration
============

Similar to :ref:`handlers`, the result of certain resource evaluations, particularly shell commands, can be easily
accesssed in Python as follows:

.. code-block:: python

    def main(self):
        cmd = Shell('date', ignore_errors=True)
        Echo("{{ cmd.rc }}")
        Echo("{{ cmd.data }}")
        if cmd.rc == 52:
            # anything is possible
            pod.bay.doors.open(im_sorry='dave')
            return

.. note:
    Registration is most commonly used with shell commands. Most resources will probably not have very interesting 
    return data other than the 'changed' attribute mentioned in :ref:`handlers`.

.. _ignore_errors:

Ignore Errors
=============

Most commands will intentionally stop the execution of an OpsMop policy upon hitting an error, by raising an exception of subclass ProviderError. A common
example would be Shell() return codes. While this exception can be caught, it can also be ignored.

.. code-block:: python

    def main(self):
        try:
            Shell("ls foo | wc -l", register="line_count", ignore_errors=True),
        except ProviderError:
            pass

.. code-block:: python

    def main(self):
        line_count = Shell("ls foo | wc -l", ignore_errors=True),
        Echo("{{ line_count.data }}")
           
.. _changed_when:

Change Reporting Control
========================

Normally, a resource will mark itself as containing changes if it performs any actions to the system.
Presence of these changes are used to decide whether to notify :ref:`handlers`.

Sometimes, particularly for shell commands, this is not appropriate, and the changed status
should possibly depend on specific return codes or output. The state can be overriden as follows:

.. code-block:: python

    def main(self):
        cmd = Shell("/bin/foo --args", changed_when=lambda x: 'changed' in x.data)
        if cmd.changed:
            Service("blippy", restarted=True)

Changed reporting control isn't really required, because you could also write things like this:

.. code-block:: python

    def main(self):
        cmd = Shell("/bin/foo --args", changed_when=changed_test)
        if "changed" in cmd.data:
            Service("blippy", restarted=True)

This is cleaner, but will result in potentially misleading output in the OpsMop command line tool.

.. _extra_vars:

CLI Extra Variables
===================

It is possible (both for ref:`local` and :ref:`push`) to specify extra variables on the command line.  These appear in templates as well as conditionals, and override
any variable value in OpsMop.

Examples::

    python3 deploy.py --apply --push --extra-vars "version=1.2.3.4 package=foo"

    python3 deploy.py --apply --push --extra-vars @vespene.json

Using the "@" symbol allows variables to be loaded from a file.  ".json", ".toml", and ".yaml" files are all readable, assuming they have the appropriate extensions.

Next Steps
==========

* :ref:`modules`
* :ref:`facts`
* :ref:`development`
* :ref:`api`


