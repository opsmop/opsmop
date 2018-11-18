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

Many simple configurations in OpsMop may simply use modules like
:ref:`module_service`, :ref:`module_package`, and :ref:`module_file`, and 
will not need all of these features, but it is also likely that every OpsMop
configuration will want to use at least some of the features explained below.

OpsMop encourages random-access learning.

The language examples below will refer to many modules detailed further in the :ref:`modules` section, so 
feel free to jump back and forth. The best way to understand these features is to consult
the `opsmop-demo <https://github.com/opsmop/opsmop-demo>`_ repo on GitHub, and also as you 
read through :ref:`modules`, you will see some of these features used in the examples in context.

Many of the examples below are contrived and don't deploy real applications, but are constructed to teach 
lessons about things such as :ref:`var_scoping` or :ref:`conditionals`.  Real OpsMop policies
for deploying an application stack would be a bit longer and would use a larger mixture of modules in concert.

By studying these examples though, you can quickly experiment and try to put
them together in your own :ref:`policy` configurations.

OpsMop does not believe you should need an extremely large library of example configurations, we want you to learn
the tool and be able to easily construct your own.

.. _method:

Provider Selection
==================

We've discussed Types a bit already.

When we talk about things like "File()", "Service()", or "Package()" in OpsMop, we call them resources,
but really resources come in two parts - Types and Providers.

Often, :ref:`types` may be coded to return only one provider.  Other modules may choose a default based
on the operating sysstem. As an example, the File() resource has only one implementation but there will be
many different implementations for Package().

Providers are the implementation code that make system changes as expressed in a Type.  The Type just defines
the request.

To install a package using the default *Provider*, we don't have to do anything special:

.. code-block:: python

    def set_resources(self):
        return Resources(
            Package(name="cowsay")
        )

However, the default type is not always the one you will want to use.  For instance, the default
Package provider on Ubuntu would be "apt", and on CentOS 7 it would be "yum", but what if we wanted
to install a package from Python's pip?

To specify or force a specific provider:

.. code-block:: python
    
    def set_resources(self):
        return Resources(
            Package(name="pygments", method="pip")
        )

NOTE that at this point in OpsMop's development, we have a lot of providers to add for packages yet.
This makes a great point of contribution, so if you are interested, see the :ref:`community` section.

Ok, so that's how to pick a stock provider.

It's also possible to use a provider that OpsMop doesn't ship with, perhaps one that you wrote for
some of your own internal services:

.. code-block:: python

    def set_resources(self):
        return Resources(
            Package(name="cowsay", method="your.custom.provider.spork")
        )

Expressing that full path for the provider name is verbose (and subject to typos), so it helps to save those strings to a python constant
to improve readability.

.. code-block:: python
    
    Package(name="cowsay", method=SPORK)

.. note:

    OpsMop is very new so providers will be growing rapidly for modules.  These are a great
    first area for contributions if you have needs for one.  See :ref:`development`.

.. note:

    It is deceptive to assume a package name is the same on all platforms.  Conditionals and various
    other systems allow solutions, but in the most common cases, your site content will just need
    to code for the platform you use.  While multi-platform content is interesting, if you don't need
    it, don't worry about it.

.. _var_scoping:

Variable Scoping
================

OpsMop uses variables in both templates and conditionals.

We've already talked a little bit about variables, and knowledge of variables weighs in on
future sections and nearly everything in OpsMop.  

It is important to not confuse Python variables with OpsMop variables.  To transfer a Python class variable
or global variable into OpsMop template space, use :ref:`module_set`.

OpsMop has a very simple to understand variable system based on the
concept of scope.  Variables defined at outer scopes are always available further
down, but changing a variable inside a scope does not effect the value at the outer scope.
These variables are 'scope-local'.

In the opsmop-demo repository, `var_scoping.py <https://github.com/opsmop/opsmop-demo/blob/master/content/var_scoping.py>`_ demonstrates
the various variable scopes in OpsMop. 

Because this is a long example, we'll refer you to GitHub and ask you to read and perhaps run the example. In browsing
the source, you will understand more about what is possible with variable scopes.

.. _eval:

Eval
====

Similar to T(), a computation of two variables is doable with Eval:

.. code-block:: python

    def set_resources(self):
        return Resources(
            Set(a=2, b=3),
            Echo(Eval("a + b"))
        )

The difference with Eval() vs "T()" is that Eval can return native python types, whereas T() always
returns a string.  Here is a contrived example:

.. code-block:: python

    def set_resources(self):
        return Resources(
            Set(a=2, b=3),
            Set(c=Eval('a+b')),
            Debug(a, b, c)
        )

In the above example, 'c' would be set to the number 5, not the string "5" (or worse, the string "23")

Where would you use this directly? Probably not very often. 

Eval is used to implement :ref:`conditionals`, described below.

.. _conditionals:

Conditions
==========

Any role, policy, or resource can be given a conditional.  If the conditional is true, that object 
will be skipped during the check or apply phase.

Expressions are specified with "when=", and accept valid `Jinja2 <http://jinja.pocoo.org/docs/>`_ expressions.  This is technically
implemented using :ref:`eval` but leaving off Eval is provided as syntactic sugar:

.. code-block:: python

    # ...    
    Shell("reboot", when="a > b")
    # ...

This is the same as the overly redundant:

.. code-block:: python

    # ...
    Shell("reboot", when=Eval("a > b"))
    # ...

And while it serves no purpose that couldn't be achieved with a comment, technically this also disables
a resource:

.. code-block:: python

    # ...
    Shell("reboot", when=False)
    # ...

.. note::
    Development info: Both Eval() and T() are implementations of the class "Lookup", and you can write your own
    subclasses of Lookup if you wish to write any kind of runtime lookup into an external system.
    See :ref:`development`.

.. note::
    Python developers will be interested to know you can save common conditions to package or class variables, including
    Eval expressions.

.. note::
    Referencing an undefined variable in a condition will intentionally result in an error. This may be avoided
    by using `Jinja2 <http://jinja.pocoo.org/docs/>`_ to select defaults. However, you could also just define a default with :ref:`module_set`
    prior to doing a 'register' call (see :ref:`registration`) and make things easy. That way, all variables will have defaults
    and you don't have to express the default from within a template.  This tip also works for general templating
    advice.

.. _nested:

Nested Scopes
=============

Nested Scopes created a quickly way of adding :ref:`conditionals` to a large number of resources:

.. code-block:: python

    def set_resources():
        return Resources(
           Resources(
               Shell("echo /tmp/motd"),
               Shell("uptime"),
               Shell("date"),
               when='F.is_linux()'
           ),
           Resources(
               Echo("nope"),
               Echo("skipping this too"),
               when='not F.is_linux()'
           )
        )


Nested scopes can also be used for variable handling, as 
demoed in 'var_scoping' in the opsmop-demo repository.

.. _registration:

Registration
============

The value of one command may be saved and fed into the output of another. 

This value is entered into local scope, and can be saved into global scope using SetGlobal(), 
which is described in a later chapter:

.. code-block:: python

    def resources(self):
        return Resources(
            Shell('date', register='date'),
            Debug('date'),
            Echo("{{ date.rc }}"),
            Echo("{{ date.data }})
        )

Registration works well with coupled with :ref:`conditionals`, :ref:`failed_when` and :ref:`changed_when`.
Some of these examples are shown in the 'opsmop-demo' repo.

.. note:
    Using Echo to show templates on the screen is a useful debug technique, but the :ref:`module_debug` module is 
    better.

.. note:
    Depending on resource, the value "rc" or "data" may be None. Register is most commonly
    used with shell commands. Providing methods on the returned result to provide
    access to the 'changed or not' status may occur in a later version.

.. _ignore_errors:

Ignore Errors
=============

Most commands will intentionally stop the execution of an OpsMop policy upon hitting an error. A common
example would be Shell() return codes. This is avoidable, and quite useful in combination with the register
command.  This is demoed in the :ref:`module_shell` documentation.

.. code-block:: python

    def resources(self):
        return Resources(
            Shell("ls foo | wc -l", register="line_count", ignore_errors=True),
            Echo("line_count.data")    
        )


.. _changed_when:

Change Reporting Control
========================

NOTE: this is a pending feature - this feature will be released shortly.

A resource will mark itself as containing changes if it performs any actions to the system.
These changes are used to decide whether to notify :ref:`handlers`.

Sometimes, particularly for shell commands, this is not appropriate, and the changed status
should possibly depend on specific return codes or output. The state can be overriden as follows:

.. code-block:: python

    Shell("/bin/foo --args", register="x", ignore_errors=True, changed_when="'changed' in x.data", notify="some_step")

If not using handlers, the change reporting isn't too significant, but it will affect CLI output counts at
the end of the policy execution.  Some users like their policies to report no changes when nothing really
happened, and that's a good practice.

.. _failed_when:

Failure Status Overrides
========================

NOTE: this is a pending feature - this feature will be released shortly

By default if a command returns a fatal error, the program will halt at this step.  This is not
always good, as sometimes, failure should depend on something other than that error status.

For instance, the following is equivalent to :ref:`ignore_errors`:

.. code-block:: python
    
    Shell("/bin/foo --args", register="x", failed_when=False)

However, that's a weird example! In a more practical example, suppose we have a shell command that
is programmed incorrectly and returns 5 on success:

.. code-block:: python

    Shell("/bin/foo --args", register="x", failed_when="x.rc != 5")

Ok, that's ALSO a weird example.  What if we have a shell command that we should consider failed
if it doesn't contain the word "SUCCESS" in the output?  Easy:

.. code-block:: python
    
    Shell("/bin/foo --args", register="x", failed_when="not 'SUCCESS' in data")

It may also be clearer to save the conditional string to a class or
package variable and use it this way:

.. code-block:: python

    Shell("/bin/foo --args", register="x", failed_when=SUCCESS_IN_OUTPUT)

Because OpsMop is python it is very easy to do those things, and we recommend it assinging to variables
for clarity when possible.

Next Steps
==========

* :ref:`modules`
* :ref:`development`
* :ref:`api`


