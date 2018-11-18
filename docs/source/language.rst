.. image:: opsmop.png
   :alt: OpsMop Logo

.. _language:

Language
--------

OpsMop configurations are written in a Python 3 DSL.

You've hopefully already read ":ref:`local`" to understand what the command line commands are 
and are ready to see what the language is about.

In another tab, please open `the opsmop-demo repository <https://github.com/vespene-io/opsmop-demo/tree/master/content>`_. In particular, see 
minimal `hello.py <https://github.com/vespene-io/opsmop-demo/blob/master/content/hello.py>`_.  All of these examples are runnable
on your computer from an OpsMop checkout.

.. _policy:

Policy
======

Policies are the top level objects in OpsMop.  Policies describe what :ref:`roles` get applied to a system being configured.

Read `hello.py <https://github.com/vespene-io/opsmop-demo/blob/master/content/hello.py>`_ to see this structure in full.
Below, we'll talk about a few parts of that file.

Since OpsMop is Python, we always start by importing some classes. The following import is syntactic sugar to import the
most commonly used classes:

.. code-block:: python

    from opsmop.core.easy import *

If you had written your own types, or wanted to pull in *any* python library at all, you could also do this here.

All policy files must contain a 'main' function which returns either a *Policy* object or a list of *Policy* objects.
This main function does *NOT* need to be surrounded in the usual 'if __name__' pattern commonly found in Python files,
nor do you need to call this function.  The opsmop CLI (see :ref:`local`) will call it for you.

.. code-block:: python

    class Hello(Policy):
  
        def set_variables(self):
            return dict()

        def set_roles(self):
            return Roles(HelloRole())
   
    def main():
        return Hello(say='Congratulations')

Take note of 'set_variables' and 'set_roles'.  Assigning variables in a Policy declaration is optional, but roles are not.
Why? A policy without roles has nothing to do!  We'll get to :ref:`roles` very shortly.

Python developers should note that objects in OpsMop have "args, kwargs" constructors, which means
you can pass a list of roles to the Roles() collection instead of listing them all inside the constructor.  
This means you can dynamically return a list of Roles from arbitrary code very easily:

.. code-block:: python

    def set_roles(self):
        roles = [ HelloRole() ]
        return Roles(**roles_list)

That example is critical to the purpose of OpsMop!  While some configuration management systems mostly
interface with humans writing content for them, any point in OpsMop can be grafted cleverly into software.
It is a cyborg automation system. So if you wanted to source your roles by talking to another system, you can do that.
You aren't limited to just using constructs provided by the Opsmop system.

Let's continue.

.. _roles:

Roles
=====

Roles describe what a configuration really does, and are the reusable core of OpsMop.  Let's look at a simple
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

Here we are doing something pretty basic, copying a file (see :ref:`module_file`). If we wanted to perform any
actions explicitly when he file changed - and not if it did not change, we could use :ref:`handlers`, which are covered
just a bit later.

Notice that we define resources in roles, but you can't assign a resource to a policy any other way. Opsmop mandates
the usage of roles as a mechanism of organization, but you can of course still only have one role in a policy you want.

Typically a role would describe an application, but it might also describe something like a common security policy, setting
up a user, and more.  THere are really no required conventions.

.. _note:
    The method 'set_variables()' and 'set_handlers()' methods can always be omitted.  The method 'set_resources()' cannot.
    
.. _types:

Types (Resources Intro)
=======================

As shown above with "File()", the set_resources() method in a role returns a collection of "Type" instances.
We casually call them Resources, but technically the Policy and Roles are also resources.  Types are something
more specific.

What are Type instances? 

OpsMop plugins come in two parts: Types and Providers.  Types, like "File()" above
describe a configuration intent - what we want to do to the system. 

Providers are implementations of the 'how', and fulfill the parameters passed to the providers.
If writing OpsMop language, you will never see a provider.  They are beneveloent configuration 
spirits running behind the scenes.  They are what actually make the changes.

Here is another example of a file resource, this time not copying a file, but merely
adjusting metadata:

.. code-block:: python

    def set_resources(self):
        return Resources(
            File(name="/tmp/foo.txt", owner='root', group='wheel', mode=0x755)
        )

Here we are using the same File resource as above, but using a few more parameters.

For those interested in :ref:`development`, the file type is "opsmop.types.file.File" and the implementation
behind the code is "opsmop.providers.file.File".  While technically the provider code COULD live in the same
file, for any modules in the core distribution of OpsMop, that never happens.

Another gotcha is of course that not all types have just one implementation.  For instance a Package could be installed
by yum, apt, or maybe pip or npm.  For details on how that works, see :ref:`method`.

The :ref:`modules` documentation shows all of the types available in the core distribution.  Currently, this list is small
as OpsMop is under early (but extremely rapid) development.  Adding a new type and provider can often be done very quickly
thanks to the object model behind OpsMop.

When you review the module documentation, you will also see many common parameters exist on all Types, driving such features as conditionals, variable registration, and more.
These will be described in :ref:`advanced` and also demoed and featured in the :ref:`modules` documentation.

.. _handlers:

Handlers
========

Roles can also declare handlers. The Handlers section is just like the regular Resources section, except that handlers run only when resources
are changed by OpsMop. When OpsMop evaluates a resource, it determines a plan for that resource (in check or apply mode), and then
executes that plan (if in apply mode). Again, review :ref:`local` for the differences in the CLI invocations for each. 
If actions are to be taken, all handlers that match the given signaled names will fire
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

.. note::
    Currently one role cannot define handlers for events signaled by another role.  They are tightly
    namespaced. 

Variables
=========

The method 'set_variables' on a Resource or a Role can define variables, and roles can also be set as parameters
when instantiating a Role::

    def set_variables(self):
        return dict(a=1, b=2, c=3)

While simply returning a dictionary is fine, it's also possible to consult any external system for loading
up those variables.  This is, of course, a completely live Python function.  If you prefer to keep your
variables in CSV or JSON or YAML or XML files - a database - or to fetch them from a REST call, it is always
up to you.

These variables are best showcased with a more involved example, so know that they exist, read on,
and in a bit prepare to dig into the example on :ref:`var_scoping`, which goes fully in on all the different
places variables can be set.

:ref:`facts` are also another way to get dynamic information into the system. Technically, ref:`facts` are not variables, 
they are really functions - but they are like variables that are always accessible in templates and conditionals. 
You will see more about facts as you browse the examples in the 'opsmop-demo' repository.  Facts also play a very
strong role in provider selection, as detailed in :ref:`method`.

.. _templates:

Templates
=========

The most common (but not only) way to use variables in OpsMop are with templates.

Templates take variables and inject them into strings. Because Templates apply to not just
the :ref:`module_file`, but also other parts of OpsMop, they warrant a section in the language guide.

OpsMop uses `Jinja2 <http://jinja.pocoo.org/docs/>`_ for templating, which is a powerful 
templating language that has quite a few capabilities beyond simple substitution, conditions, and loops.

The most basic use of Jinja2 is variable substitution, for instance in a config file it might look like::

    marzlevanes=6
    defrobinicate="{{ defrobnicate }}"
    realign_main_deflector_array=True
    excelsior="{{ excelsior }}"

There are also conditionals, loops, and more.

The most common way of using templating is the :ref:`module_file`:

.. code-block: python
  
    def set_resources(self):
        return Resources(
            File(name="/etc/foo.conf", from_file="templates/foo.conf.j2")
        )

It is important to understand templating in OpsMop works differently than in some other config systems. It is more explicit.
To avoid ambiguity, OpsMop does not automatically template every string. Only a few certain utility modules automatically assume their inputs are templates. 
One is :ref:`module_echo`:

.. code-block:: python

    def set_resources(self):
        return Resources(
            Echo("My name is {{ name }}")
        )

To explictly template a string for some other parameter, we need to use 'T()':

.. code-block:: python

    def set_resources(self):
        return Resources(
            Package(name="foo", version=T("{{ major }}.{{ minor }}"))
        )

Any variable in the current scope is available to 'T()'.
However, python variables are actually not.  To make them available to OpsMop you would need to add
them to the local scope:

.. code-block:: python

    def set_resources(self):
        return Resources(
            Set(foo_version=foo_version),
            Package(name="foo", version=foo_version)
        )

.. note::
    Use of an undefined variable in a template will intentionally cause an error.
    This can be handled by using filters in Jinja2 if you need to supply a default.
    This feature, while it may seem annoying, is actually a very good thing - you don't
    want an installation to continue with an improperly configured config file, when
    certain values are mysteriously blank.

.. note::
    Because template expressions are late binding, they will push some type-checking that would
    normally happen at validation to 'check' or 'apply' stages to runtime evaluation. To review, 
    see :ref:`local`. For example, if this
    file was missing, it might not be determined until halfway through the evaluation of a policy::

        File(name="/etc/foo.cfg", from_file=T("files/{{ platform }}.cfg"))

    This is usually completely safe if you understand all possible values of the variable. In the worst case,
    it will produce a runtime error if the file could not be found.

In Summary
==========

Policies, Roles, Types, and Handlers - along with Variables and Templates - make up the key concepts of OpsMop. 

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

