Language
========

Please reference `the opsmop-demo repository <https://github.com/vespene-io/opsmop-demo/tree/master/content>`_ while reading
this chapter, in particular `hello.py <https://github.com/vespene-io/opsmop-demo/blob/master/content/hello.py>`_ for the most
minimal language example. Other files in that directory show more advanced language features.

Policy
======

OpsMop configuration policies are expressed in a Python DSL.

Typically policies contain the following import to load in a wide array of useful OpsMop classes. Use of your own
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

A policy class *may* define a seperate set_variables() method that returns further variables, perhaps
fetched from an environment or external system.

A policy class *must* define a set_roles() method, which returns a collection of roles that describe
the configuration of that policy. Using only one role is acceptable.

Role
====

Roles are the core of OpsMop::

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

You can see roles instantiated in the "set_roles()" method of the Hello policy above. Roles, like Policies,
can also take key=value arguments in their constructor to established scoped variables. Also, like Policies,
roles *may* define a set_variables() method that returns additional variables, potentially sourced from
external systems.

Roles *must* define a set_resources method, which returns a collection of Resource objects, that actually
describe what the role will do.

Technically resources can also be nested, which allows a way to attach parameters to multiple resources in a block.
This is covered in some of the content in the example repo, and is not neccessary in most installations. For instance,
nested resources can be used to implement tight variable scoping, or assign one conditional to multiple resources
simultaneously.

Types
=====

The set_resources() method in a role will return a collection of type instances.

OpsMop plugins are in two parts: Types and Providers.  Types, like "File"
describe a configuration intent and can take a variety of parameters::
            
    File(name="/tmp/foo.txt", from_content=msg)

Similarly::

    File(name="/tmp/foo.txt", owner='root', group='wheel', mode=0x755)

Additionally, common parameters exist, driving such features as conditionals, variable registration, and more.
These will be described below.

The OpsMop policy language works with types, whereas providers are the implementation behind
those types that actually performs the work.

So what we are doing right now is saying "the file should look like this", but the behavior is not implemented
in that "File()" class - it's in the provider.  This is covered later in :ref:`plugin_development`.

Provider Selection
==================

Often, a Type may be coded to return a default provider on a specific platform, but this is always
overrideable, either with one of the providers that ship with OpsMop or your own. To install a package
using the default provider for the operating system::

    Package(name="cowsay")

This would usually select "yum", "apt", or "brew" on CentOS, Ubuntu, or OS X, respectively.

To specify or force a specific provider::

    Package(name="cowsay", method="yum")

To specify a provider OpsMop doesn't know about, it's still possible to select one out of tree::

    Package(name="cowsay", method="your.custom.provider.spork")

Expressing that full path is verbose, so it helps to save those strings to a python constant.
    
    Package(name="cowsay", method=SPORK)

This is a good reminder that 100% of everything in OpsMop is scriptable and subclassable.

Variable Scoping
================

We've already talked a little bit about variables, and knowledge of variables weighs in on
future sections.

In the opsmop-demo repository, `var_scoping.py <https://github.com/vespene-io/opsmop-demo/blob/master/content/var_scoping.py>`_ demonstrates
the various variable scopes in OpsMop. 

Templates
=========

Sometimes you will want to inject a variable into a string.

OpsMop uses Jinja2 for templating, but does not automatically template every string.

Only a few certain utility modules automatically assume their inputs are templates::

    Echo("My name is {{ name }}")

To explictly template a string:

    Package(name="foo", version=T("{{ major }}.{{ minor }}"))

The value "T" is a late binding indication that the value should be templated just
before check-or-apply mode application.

Warning: Because template expressions are late binding, they will push some type-checking that would
normally happen before check-and-apply stages to runtime evaluation. For example, if this
file was missing, it might not be determined until halfway through the evaluation of a policy::

    File(name="/etc/foo.cfg", from_file=T("content/{{ platform }}.cfg"))

Eval
====

Similar to T(), a computation of two variables is doable with Eval::

    Echo(Eval("a + b"))

The difference with Eval() vs "T()" is that Eval can return native python types, whereas T() always
returns a string.

Conditions
==========

Any role, policy, or resource can be given a conditional.  If the conditional is true, that resource
and resources therein will be skipped during the check or apply phase.

Expressions are specified with "when=", which accepts legal Jinja2 expressions.  This is technically
implemented using Eval() but leaving off Eval is provided as syntactic sugar::

    Shell("reboot", when="a > b")

This is the same as the overly redundant::

    Shell("reboot", when=Eval("a > b"))

Bonus: Both Eval() and T() are implementations of the class "Deferred", and you can write your own
subclasses of Deferred if you wish to write any kind of runtime lookup into an external system.
See :ref:`plugin_development`.

Facts
=====

Facts are information about the system, including information like the OS version and architecture,
that are discovered by OpsMop dynamically at runtime.  

The facts implementation of OpsMop uses on-demand memoization, so the cost of computing an expensive 
fact will not be realized unless it is actually referenced.

Facts are accessed by using the "F" accessor in the policy language, and can be used anywhere::

    Echo("The OS type is {{ F.os_type }}")

Here is a conditional:

	Echo("I am Linux", when="F.is_linux")

Registration
============

The value of one command may be saved and fed into the output of another. This value is entered into
local scope, and can be saved into global scope using SetGlobal, which is detailed in a later chapter::

    Shell("date", register="date"),
    Echo({{ date.rc }}),
    Echo("{{ date.data }}"),

Ignore Errors
=============

Most commands will intentionally stop the execution of an OpsMop policy upon hitting an error. A common
example would be Shell() return codes. This is avoidable, and quite useful in combination with the register
command.

    Shell("ls foo | wc -l", register="line_count", ignore_errors=True)
    Echo("{{ line_count.data }}")    

Signals
=======

Handler objects, described above, are resources that only activate when another resource reports having
changed the system. Resources mark change any time they fulfill an action that they have planned.

	File("/etc/foo.conf", from_template="templates/foo.conf.j2", signals="restart foo app")

Signals will cause the corresponding handler to fire, for instance, if the Role defines some handlers 
like so::

    set_handlers(self):
        return Handlers(
           restart_foo_app = Service(name="foo", restarted=True) 
        )

Then the restart command would only one if some resource with the designated 'signals' parameter
indicated some change was neccessary. In the above example, if the configuration file already had
the correct contents, it would not request a restart of the service.

Next Steps
==========

* :ref:`main`
* :ref:`aux`
* :ref:`plugin_development`

