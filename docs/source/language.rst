Language
========

OpsMop configuration is expressed in a Python DSL.

This documentation works best if you have another tab open. Please reference 
`the opsmop-demo repository <https://github.com/vespene-io/opsmop-demo/tree/master/content>`_ while reading
this chapter, in particular `hello.py <https://github.com/vespene-io/opsmop-demo/blob/master/content/hello.py>`_ for the most
minimal language example. Other files in that directory show more advanced language features.

.. _policy:

Policy
======

Pull up `hello.py <https://github.com/vespene-io/opsmop-demo/blob/master/content/hello.py>`_ and skim the source.

The top-level objects in OpsMop are *Policies*, and a configuration can load in more than one of them.
It is fine to refer an opsmop python file *as* a policy, even if it instantiates one or more Policy objects.

Since OpsMop is Python, nothing can do anything if we don't import some useful tools. Typically policies contain 
the following import to load in a wide array of useful OpsMop classes. Use of your own
objects and imports is 100% encouraged, but often not required::

    from opsmop.core.easy import *

All policies contain a main function which return either a Policy object or a list of Policy objects::

    class Hello(Policy):
  
        def set_variables(self):
            return dict()

        def set_roles(self):
            return Roles(HelloRole())
   
    def main():
        return Hello(say='Congratulations')

A policy constructor *may* take key-value parameters to set variables usable throughout the policy.

A policy class *may* also define a seperate set_variables() method that returns further variables, perhaps
fetched from an environment or external system.

A policy class *must* define a set_roles() method, which returns a collection of roles that describe
the configuration of that policy. Using only one role is acceptable. Why? A policy without roles has
nothing to do.  Of course, you could be sneaky and define no roles at all. The system would tolerate that.
But it would be boring.

Let's continue.

.. _its_python:

Aside: Info for Python Developers
=================================

The examples we're showing are 'easy mode'  and are about to show are all constructed in a fairly common way. 
However, it's important to remember that OpsMop is fully programmable too.

If you want to put your roles in different files, or define them *after* your policy, the system is Python, and does
not enforce any particular style.  Any packages you may import need to be part of your PYTHONPATH, however.
You can subclass anything.

Python developers may also wish to note that any Collection objects, like Roles, take Pythonic args,
which means you can feed lists to them::
        
    def set_roles(self):
        return Roles(*role_list)

Why? OpsMop is a bit of a cyborg system - it is partly for humans, and partly for machines. Unlike
many other configuration systems, we often expect your policies may programatically deside to
be different, based on any external system, and they can if you so wish. Code generation is
simply not neccessary to create dynamically-behaving policies. 

If your 'set_roles' method wants to load up an XML file to decide to build out some roles, that's ok,
we won't judge. Ok, we will - but you can do it! 

Later in the :ref:`plugin_development` guide we'll talk about extending the rest of OpsMop.

.. _roles:

Roles
=====

Roles are the reusable core of OpsMop::

    class HelloRole(Role):

        def set_variables(self):
            return dict(program='OpsMop')

        def set_resources(self):

            msg = T("Hello {{ program }} World! {{ say}}!")

            return Resources(
                File(name="/tmp/foo.txt", from_content=msg)
            )

        def set_handlers(self):
            return Handlers()

You can see role instances are instantiated in the "set_roles()" method of the Hello policy above. Roles, like Policies,
can also take key=value arguments in their constructor to established scoped variables. Also, like Policies,
roles *may* define a set_variables() method that returns additional variables, potentially sourced from
external systems.

Roles *must* define a set_resources method, which returns a collection of Resource objects, that actually
describe what the role will do.

Technically resources can also be nested, which allows a way to attach parameters to multiple resources in a block(F.os_type). 
This is covered in some of the content in the example repo, and is not neccessary in most installations. For instance,
nested resources can be used to implement tight variable scoping, or assign one conditional to multiple resources
simultaneously.

If you are getting lost, refer back to the example repo and skim it - and seeing it all in context should help it
sync in.

.. _types:

Types
=====

The set_resources() method in a role will return a collection of type instances.

What are type instances?

OpsMop plugins are in two parts: Types and Providers.  Types, like "File"
describe a configuration intent and can take a variety of parameters::
            
    File(name="/tmp/foo.txt", from_content=msg)

Similarly::

    File(name="/tmp/foo.txt", owner='root', group='wheel', mode=0x755)

Additionally, common parameters exist, driving such features as conditionals, variable registration, and more.
These will be described in :ref:`advanced`.

The OpsMop policy language works with types, whereas providers are the implementation behind
those types that actually performs the work - when writing a *Policy* these are not interacted with directly.

So what we are doing right now is saying "the file should look like this", but the behavior is not implemented
in that "File()" class - it's in the provider code.  This is covered later in :ref:`plugin_development`.

.. _handlers:

Handlers
========

The handlers section is just like the regular resources section, except that handlers run only when events change being notified
by a 'signal' from a resource::

     def set_resources():
         return Resources(
             File(name="/etc/foo.conf", from_template="templates/foo.conf.j2", signals="restart_foo")
         )

     def set_handlers():
         return Handlers(
             Service(name='foo', state='restarted')
         )

Next Steps
==========

* :ref:`modules`
* :ref:`advanced`
* :ref:`plugin_development`

