.. _advanced:

Language Part 2
---------------

Once you have covered the basics of the language in :ref:`language`, here are some additional
advanced language features you may be interested in.

We say these are 'advanced' features not because they are complicated, but just because they
are optional.  

The most simple configurations in OpsMop will simply use modules like
:ref:`module_service`, :ref:`module_package`, and :ref:`module_file`, and 
will not need all of these features, but it is also very likely that every OpsMop
configuration will use at least some of these.

OpsMop encourages random-access learning.

The language examples will refer to many modules detailed further in the :ref:`modules` section.
Feel free to jump back and forth. The best way to understand these features is to consult
the `opsmop-demo <https://github.com/vespene-io/opsmop-demo>`_ repo on GitHub, and also as you 
read through :ref:`modules`, you will see some of these features used in the examples in context.

Some of these examples are contrived and don't deploy real applications, but are constructed to teach 
lessons about things such as :ref:`variable_scoping` or :ref:`conditionals`.  

By studying these examples, you can quickly experiment and try to put
them together in your own :ref:`policy` configurations.

.. _method:

Provider Selection
==================

Often, :ref:`types` may be coded to return a default *Provider* on a specific platform.  Providers
are the implementation code that make changes expressed in a Type.

Many Types have only one provider, but many Types, especially :ref:`module_service` will have many different
ones.

To install a package using the default *Provider*, we don't have to do anything special:

.. code-block:: python

    def resources(self):
        return Resources(
            Package(name="cowsay")
        )

However, the default type is not always the one you will want to use.  For instance, the default
Package provider on Ubuntu would be "apt", but what if we wanted to install a package from Python's 
pip?

To specify or force a specific provider:

.. code-block:: python
    
    def resources(self):
        return Resources(
            Package(name="pygments", method="pip")
        )

To specify a provider OpsMop doesn't know about, it's still possible to select one out of tree:

.. code-block:: python

    Package(name="cowsay", method="your.custom.provider.spork")

Expressing that full path for the provider name is verbose (and subject to typos), so it helps to save those strings to a python constant
to improve readability.

.. code-block:: python
    
    Package(name="cowsay", method=SPORK)

.. note:

    OpsMop is very new so providers will be growing rapidly for modules.  These are a great
    first area for contributions if you have needs for one.  See :ref:`development`.

.. _var_scoping:

Variable Scoping
================

We've already talked a little bit about variables, and knowledge of variables weighs in on
future sections and nearly everything in OpsMop.  

OpsMop has a very simple to understand variable system based on the
concept of scope.  Variables defined at outer scopes are always available further
down, but changing a variable inside a scope does not effect the value at the outer scope.
These variables are 'scope-local'.

In the opsmop-demo repository, `var_scoping.py <https://github.com/vespene-io/opsmop-demo/blob/master/content/var_scoping.py>`_ demonstrates
the various variable scopes in OpsMop. 

Because this is a complex example, we'll refer you to GitHub and ask you to run the example.

.. _templates:

Templates
=========

The :ref:`var_scoping` shows that variables can be set in many places.  But what good are variables if you can't use them?

Ref :ref:`conditionals` are one way to use variables, but the most common way would be templates.
Templates take  variables and inject them into strings.

OpsMop uses Jinja2 for templating, which is a powerful templating language that has quite a few capabilities
beyond simple substitution, conditions, and loops.

The most basic use of templating is in the file module:

.. code-block: python
  
   Template(name="/etc/foo.conf", from_file="templates/foo.conf.j2")

See :ref:`module_file` for more information.

It is important to understand templating in OpsMop works differently than in some other systems. It is more explicit.
OpsMop does not automatically template every string. Only a few certain utility modules automatically assume their inputs are templates. 
One is :ref:`module_echo`:

.. code-block:: python

    Echo("My name is {{ name }}")

To explictly template a string for some other parameter, we have to use 'T()':

.. code-block:: python

    Package(name="foo", version=T("{{ major }}.{{ minor }}"))

The value "T" is a late binding indication that the value should be templated just
before check-or-apply mode application. Any variable in the current scope is available to 'T()'.
However, python variables are actually not.  To make them available to OpsMop you would need to add
them to the local scope:

.. code-block:: python

    Set(foo_version=foo_version),
    Package(name="foo", version=foo_version)

.. note::
    Use of an undefined variable in a template will intentionally cause an error.
    This can be handled by using filters in Jinja2 if you need to supply a default.

.. note::
    Because template expressions are late binding, they will push some type-checking that would
    normally happen before check-and-apply stages to runtime evaluation. For example, if this
    file was missing, it might not be determined until halfway through the evaluation of a policy::

        File(name="/etc/foo.cfg", from_file=T("files/{{ platform }}.cfg"))

    This is usually safe if you understand all possible values of the variable. In the worst case,
    it will produce a runtime error.

.. _eval:

Eval
====

Similar to T(), a computation of two variables is doable with Eval:

.. code-block:: python

    Echo(Eval("a + b"))

The difference with Eval() vs "T()" is that Eval can return native python types, whereas T() always
returns a string.  Here is a contrived example:

.. code-block:: python

    Set(a=2, b=3),
    Set(c=Eval('a+b')),
    Debug(a, b, c)

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

    Shell("reboot", when="a > b")

This is the same as the overly redundant:

.. code-block:: python

    Shell("reboot", when=Eval("a > b"))

And while it serves no purpose that couldn't be achieved with a comment, technically this also disables
a resource:

.. code-block:: python

    Shell("reboot", when=False)

.. note::
    Development info: Both Eval() and T() are implementations of the class "Deferred", and you can write your own
    subclasses of Deferred if you wish to write any kind of runtime lookup into an external system.
    See :ref:`development`.

.. note::
    Python developers will be interested to know you can save common conditions to package or class variables, including
    Eval expressions.

.. note::
    Referencing an undefined variable in a condition will intentionally result in an error. This may be avoided
    by using `Jinja2 <http://jinja.pocoo.org/docs/>`_ to select defaults. However, you could also just define a default with :ref:`module_set`
    prior to doing a :ref:`register` call and make things easy. That way, all variables will have defaults
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

NOTE: this is a pending feature - this feature will be released shortly.

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

Because OpsMop is python it is very easy to do those things, and we recommend it.

Next Steps
==========

* :ref:`modules`
* :ref:`development`
* :ref:`api`


