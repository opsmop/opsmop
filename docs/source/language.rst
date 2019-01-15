.. image:: opsmop.png
   :alt: OpsMop Logo

.. _language:

Language
--------

OpsMop policy files are just Python 3 scripts that contain a *Policy* defintion and *Roles* subclasses.  Roles describe what code to run on different hosts
in the OpsMop inventory.  If run locally, they apply to the local system, though push mode (see :ref:`push`) will apply them to remote
systems via SSH.

You've hopefully already read ":ref:`local`" to understand what the command line commands are 
and are ready to see what the language is about.

In another tab, please open `the opsmop-demo repository <https://github.com/opsmop/opsmop-demo/tree/master/content>`_. In particular, see 
minimal `hello.py <https://github.com/opsmop/opsmop-demo/blob/master/content/hello.py>`_.  All of these examples are runnable
on your computer from an OpsMop checkout.

.. _policy:

Policy
======

*Policies* are the top level objects in OpsMop.  *Policies* describe what :ref:`roles` get applied to a system being configured.

Read `hello.py <https://github.com/opsmop/opsmop-demo/blob/master/content/hello.py>`_ to see this structure in full.
Below, we'll talk about a few parts of that file in detail.

Since OpsMop is Python, we must always start by importing some classes. The following import is syntactic sugar to import the
most commonly used classes:

.. code-block:: python

    from opsmop.core.easy import *

If you had written your own *Types*, or wanted to pull in any python library at all, you could also import them here.

OpsMop policies are made excutable by adding a "__main__" clause that invokes the opsmop CLI code, turning a policy
file into an executable program. Here is a very basic Policy definition:

.. code-block:: python

    class Hello(Policy):
  
        def set_variables(self):
            return dict()

        def set_roles(self):
            return Roles(HelloRole())
   
    if __name__ == '__main__':
        Cli(Hello())

See :ref:`local` for how this file would be executed.  

Take special note of 'set_variables' and 'set_roles'. *Roles* are the real units of work in OpsMop. 
*Policies* say what *Roles* are applied, and optionally set some *variables*, but *Roles* will do all the work.

Assigning *variables* in a *Policy* declaration is optional, but *Roles* are not.
Why? A *Policy* without *Roles* has nothing to do!  We'll get to :ref:`roles` very shortly.

Python developers should note that objects in OpsMop have "args, kwargs" constructors, which means
you can pass a list of *Roles* to the Roles() collection instead of listing them all inside the constructor.  
This means you can dynamically return a list of *Roles* from arbitrary code very easily:

.. code-block:: python

    def set_roles(self):
        roles_list = [ HelloRole() ]
        return Roles(*roles_list)

That example is critical to the purpose of OpsMop!  While some configuration management systems mostly
are for humans writing content for them, any point in OpsMop can be grafted cleverly into software.
It is a cyborg automation system. So if you wanted to source your *Roles* (or :ref:`types`) by talking to another system, you can do that.
You aren't limited to just using constructs provided by the Opsmop system.

Sidenote: If you pass key=value arguments to a *Role* or *Policy*, it has the effect of also creating some variables, and this
is automatically possible for all *Policies* and *Roles*. Behold: parameterized values!

.. code-block:: python

    HelloRole(a=1, b=2)

Let's continue with more about Roles.

.. _roles:

Roles
=====

*Roles* describe what a configuration really does, and are the reusable core of OpsMop. Let's look at a simple
*Role* now:

.. code-block:: python

    class HelloRole(Role):

        def set_variables(self):
            return dict()

        def main(self):
            File(name="/tmp/foo.txt", from_file="files/foo.cfg")

The main function of each role can run arbitrary code, but here we are using the built-in :ref:`module_file` to copy a file over.

If used locally, this is just a copy from a relative location, but if used in :ref:`push` mode, the file would be transferred remotely.
The :ref:`modules` system in OpsMop is completely optional, but these powerful resources extend OpsMop into a full configuration and deployment system.

.. _types:

Integrated Module Library
=========================

As shown above, the classes like "File" are "Types" in the OpsMop standard module library.  

For users familiar with "classical" configuration management, these modules provide *optional* declarative, model-based configuration and
deployment features on top of the OpsMop control framework.

These OpsMop modules are implemented in two parts: *Types* and *Providers*. *Types*, like "File()" above
describe a configuration intent - what we want to do to the system. *Providers* are the implementation.

Here is another example of a File *Type*, this time not copying a file, but merely
adjusting metadata:

.. code-block:: python

    def main(self):
        File(name="/tmp/foo.txt", owner='root', group='wheel', mode=0x755)

For those interested in :ref:`development`, when you browse the :ref:`modules`, each module page
will link to the *Type* and *Provider* code (for all *Providers*) on GitHub.  This makes it easy to understand
what a *Type* and *Provider* does. 

Not all *Types* have just one *Provider* implementation.  For instance a *Package* could be installed
by yum, apt, or maybe pip or npm.  For details on how that works, see :ref:`method`.

The :ref:`modules` documentation shows all of the *Types* available in the core distribution.  Currently, this list is somewhat small
as OpsMop is under early (but extremely rapid) development.  Adding a new *Type* and *Provider* can often be done very quickly
thanks to the object model behind OpsMop. It is easy to write your own.

When you review the module documentation, you will also see many common parameters exist on all *Types*, driving such features as conditionals, variable registration, and more.
These will be described in :ref:`advanced` and also demoed and featured in the :ref:`modules` documentation.  All :ref:`modules` documentation is actually
executable in the demo repo, and this will help you understand *Types* and *Providers* as you try them out.

.. _handlers:

Handlers
========

Unlike some other configuration management systems, OpsMop module events are treated differently.

If a provider decides it needs to change the system (whether in dry-run mode or not), it will let you know.  This can be used to do things like restart
services when files change, and so on.

.. code-block:: python

     def main():
         f = File(name="/etc/foo.conf", from_template="templates/foo.conf.j2")
         if f.changed():
             Service(name='foo', restarted=True)

In the above example, if the file was different on disk than what the template wanted, we would
restart service 'foo'. If the file was already correct, the service would not be restarted.

See also :ref:`module_file` and :ref:`module_service`.

.. _templates:

Templates
=========

The most common (but not only) way to use variables in OpsMop are with templates.

Templates take *variables* and inject them into strings. Because Templates apply to not just
the :ref:`module_file`, but also other parts of OpsMop, they warrant a section in the language guide.

OpsMop uses `Jinja2 <http://jinja.pocoo.org/docs/>`_ for templating, which is a powerful 
templating language that has quite a few capabilities beyond simple substitution, conditions, and loops.

The most basic use of *Jinja2* is variable substitution, for instance in a config file it might look like::

    marzlevanes=6
    defrobinicate="{{ defrobnicate }}"
    realign_main_deflector_array=True
    excelsior="{{ excelsior }}"

There are also conditionals, loops, and more.

The most common way of using templating is the :ref:`module_file`.  In the following example variables come from either
the "set_variables" function or program scope.

.. code-block: python

    def set_variables(self):
        marzlevanes=12
  
    def main(self):
        defrobnicate='blippy'
        excelsior=True
        
        File(name="/etc/foo.conf", from_file="templates/foo.conf.j2")
        
It is important to understand templating in OpsMop works differently than in some other config systems. It is more explicit.
To avoid ambiguity, OpsMop does not automatically template every string. Only a few certain utility modules automatically assume their inputs are templates. 
One is :ref:`module_echo`:

.. code-block:: python

    def main(self):
        Echo("My name is {{ name }}")

To explictly template a string for some other parameter, we need to use 'T()':

.. code-block:: python

    def main(self):
        Package(name="foo", version=T("{{ major }}.{{ minor }}"))

.. note::
    Use of an undefined variable in a template will intentionally cause an error.
    This can be handled by using filters in *Jinja2* if you need to supply a default.
    This feature, while it may seem annoying, is actually a good thing - you don't
    want an installation to continue with an improperly configured config file, when
    certain values are mysteriously blank.


In Summary
==========

*Policies*, *Roles*, and *Types* - along with *Variables* and *Templates* - make up the key concepts of OpsMop. 

There are many advanced language features available, which you should skim to get a feel of what is possible beyond
the simple examples here. See :ref:`advanced` next.

If you have not done so already, the 'opsmop-demo' repository is an excellent resource for learning
the language, as is :ref:`modules`.  These examples will provide a better understanding when read
along with this chapter.

Additional language features in :ref:`advanced` will help you understand how to do more detailed
things with OpsMop, and are also best understood when referring to both the 'opsmop-demo' repository
and the :ref:`modules`.

If you want to know more about the internals, check out :ref:`development`.

Should you have any specific questions, we'd also encourage you to stop by the :ref:`forum` as we would
be glad to help.

Next Steps
==========

* :ref:`modules`
* :ref:`advanced`
* :ref:`development`
* :ref:`community`

