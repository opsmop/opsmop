.. _language:

Language
--------

OpsMop configurations are written in a Python 3 DSL.

You've hopefully already read :ref:`local` and are ready to see what the language is about.
If not, please do so now.

In another tab, open `the opsmop-demo repository <https://github.com/vespene-io/opsmop-demo/tree/master/content>`_. In particular, see 
`hello.py <https://github.com/vespene-io/opsmop-demo/blob/master/content/hello.py>`_ for the starter example.  You may run all of them.

.. _policy:

Policy
======

Policies are the top level objects in OpsMop.  They describe what :ref:`roles` get applied to a system being configured.

Read `hello.py <https://github.com/vespene-io/opsmop-demo/blob/master/content/hello.py>`_ to see this structure in full
context.

Since OpsMop is Python, we start by importing some classes. The following import is syntactic sugar to import the
most commonly used classes:

.. code-block:: python

    from opsmop.core.easy import *

All policy files contain a 'main' function which returns either a *Policy* object or a list of *Policy* objects:

.. code-block:: python

    class Hello(Policy):
  
        def set_variables(self):
            return dict()

        def set_roles(self):
            return Roles(HelloRole())
   
    def main():
        return Hello(say='Congratulations')

Take note of 'set_variables' and 'set_roles'.  Variables are optional, but roles are not.
Why? A policy without roles has nothing to do!  We'll get to roles shortly.

Python developers should note that objects in OpsMop have "args, kwargs" constructors, which means
you can pass a list of roles to the Roles() collection instead of listing them all inside the constructor.  
This means you can dynamically return a list of Roles from arbitrary code very easily:

.. code-block:: python

    roles = [ HelloRole() ]
    return Roles(**roles_list)

That example is critical to the purpose of OpsMop.  While some configuration management systems mostly
interface with humans writing content for them, any point in OpsMop can be grafted cleverly into software.
It is a cyborg automation system.

Let's continue.

.. _roles:

Roles
=====

Roles describe what a configuration really does, and are reusable core of OpsMop.  Let's look at a simple
role now:

.. code-block:: python

    class HelloRole(Role):

        def set_variables(self):
            return dict()

        def set_resources(self):
            return Resources(
                File(name="/tmp/foo.txt", from_file="files/foo.cfg")
            )

        def set_handlers(self):
            return Handlers()

Here we are doing something pretty basic, copying a file (see :ref:`module_file` for executable examples using
this module).

.. _note:
    The method 'set_variables()' and 'set_handlers()' methods can always be ommitted.

.. _note:
    Roles() and Policy() objects also take key=value arguments and you can parameterize them
    to set variables that way. This is demonstrated in some of the examples in the opsmop-demo repository.
    See also :ref:`var_scoping`.
    
.. _types:

Types (Resources Intro)
=======================

As shown above with "File()", the set_resources() method in a role returns a collection of "Type" instances.

What are Type instances? 

OpsMop plugins come in two parts: Types and Providers.  Types, like "File()"
describe a configuration intent - what we want to do to the system.  They encapsulate
a list of parameters that describe that intent.

Providers are implementations of the 'how', and fulfill the parameters passed to the providers.
If writing OpsMop language, you will never see a provider.  They are beneveloent configuration 
spirits running behind the scenes.

Here is another example of a file resource, this time not copying a file, but merely
adjusting metadata:

.. code-block:: python

    File(name="/tmp/foo.txt", owner='root', group='wheel', mode=0x755)

For those interested in :ref:`development`, the file type is "opsmop.types.file.File" and the implementation
behind the code is "opsmop.providers.file.File".

The trick is of course that not all types have just one implementation.  For instance a Package could be installed
by yum, apt, or maybe pip or npm.  For details on how that works, see :ref:`method`.

Further, many common parameters exist on all types, driving such features as conditionals, variable registration, and more.
These will be described in :ref:`advanced`.  These common examples are also demoed and featured in the :ref:`modules` documentation.

.. _handlers:

Handlers
========

The Handlers section is just like the regular Resources section, except that handlers run only when resources
are changed by OpsMop. When OpsMop evaluates a resource, it determines a plan for that resource (in check or apply mode), and then
executes that plan (if in apply mode).  If actions are to be taken, any handlers that match the given signal names will also fire
at the end of role evaluation.

Here is a change being notified by a 'signal' from a resource:

.. code-block:: python

     def set_resources():
         return Resources(
             File(name="/etc/foo.conf", from_template="templates/foo.conf.j2", signals="restart_foo")
         )

     def set_handlers():
         return Handlers(
             Service(name='foo', state='restarted')
         )

In the above example, if the file was different on disk than what the template wanted, we would
restart service 'foo'. If the file was already correct, the service would not be restarted.

See also :ref:`module_file` and :ref:`module_service`.

In Summary
==========

Policies, Roles, Types, and Handlers make up the key concepts of OpsMop.  There are many advanced
language features available, which you should skim to get a feel of what is possible beyond
the simple examples here. See :ref:`advanced` next.

If you have not done so already, the 'opsmop-demo' repository is an excellent resource for learning
the language, as is :ref:`modules`.  These examples will provide a better understanding when read
along with this chapter.

Additional language features in :ref:`advanced` will help you understand how to do more detailed
things with OpsMop, and are also best understood when referring to both the 'opsmop-demo' repository
and the :ref:`modules`.

If you want to know more about the internals, check out :ref:`development`.

Next Steps
==========

* :ref:`modules`
* :ref:`advanced`
* :ref:`development`

