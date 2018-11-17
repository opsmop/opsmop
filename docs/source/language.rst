.. _language:

Language
--------

OpsMop configuration is expressed in an easy to understand Python DSL.

You've hopefully already read :ref:`local` and are ready to see what the language is about.

.. note:

This documentation works best if you have another tab open. 

We suggest you reference `the opsmop-demo repository <https://github.com/vespene-io/opsmop-demo/tree/master/content>`_ while reading
this chapter, in particular `hello.py <https://github.com/vespene-io/opsmop-demo/blob/master/content/hello.py>`_ for the most
minimal language example. Other files in that directory show more advanced language features.

.. _policy:

Policy
======

Policies are the top level objects in OpsMop, and describe what :ref:`roles` get applied to a system being configured.

Please open `hello.py <https://github.com/vespene-io/opsmop-demo/blob/master/content/hello.py>`_ and skim the source to see this
in context.

Since OpsMop is Python, we must import some classes to use OpsMop. The following import is syntactic sugar to import the
most commonly used parts of OpsMop:

.. code-block:: python

    from opsmop.core.easy import *

All policies contain a main function which return either a *Policy* object or a list of *Policy* objects::

.. code-block:: python

    class Hello(Policy):
  
        def set_variables(self):
            return dict()

        def set_roles(self):
            return Roles(HelloRole())
   
    def main():
        return Hello(say='Congratulations')

Take note of 'set_variables' and 'set_roles'.  Variables are optional, but roles are not.
Why? A policy without roles has nothing to do. 

Python developers should note that objects in OpsMop are programmed as "*args, **kwargs", which means
you can pass a list of roles to the Roles() collection.  This means you can dynamically return a list
of Roles from arbitrary code very easily.

Let's continue.

.. _roles:

Roles
=====

Roles describe what a configuration really does, and are reusable core of OpsMop::

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

Here we are doing something pretty basic, creating a file based on an inline template, and then
echoing a message.  This is a contrived example.

.. _note:
    The method 'set_variables()' can always be ommitted.

.. _note:
    Roles() and Policy() objects also take key=value arguments and you can parameterize them
    to set variables that way. This is demonstrated in some of the examples in the opsmop-demo repository.
    
.. _types:

Types
=====

As shown above with "File()", the set_resources() method in a role returns a collection of "Type" instances.

What are type instances? 

OpsMop plugins come in two parts: Types and Providers.  Types, like "File()"
describe a configuration intent - what we want to do to the system.

Providers are implementations of the 'how'.

Here is another example of a file resource, this time not copying a file, but merely
adjusting metadata:

.. code-block:: python

    File(name="/tmp/foo.txt", owner='root', group='wheel', mode=0x755)

Many common parameters exist on all types, driving such features as conditionals, variable registration, and more.
These will be described in :ref:`advanced`.

.. _handlers:

Handlers
========

The handlers section is just like the regular resources section, except that handlers run only when resources
are changed by OpsMop. Here is a change being notified by a 'signal' from a resource::

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
restart service 'foo'.

In Summary
==========

Policies, Roles, Types, and Handlers make up the key concepts of OpsMop.  There are many advanced
language features available, which you should skim to get a feel of what is possible beyond
the simple examples here. See :ref:`advanced` next.

If you have not done so already, the 'opsmop-demo' repository is an excellent resource for learning
the language, as is :ref:`modules`.

If you want to know more about the internals, check out :ref:`development`.

Next Steps
==========

* :ref:`modules`
* :ref:`advanced`
* :ref:`development`

