.. _advanced:

Language Part 2
---------------

After covering the basics of the language in :ref:`language` here are some additional
advanced language features. 

Not everyone will need to make use of these, feel free to learn them as you go and
do not feel like you need to understand them or use them all at once.

The language examples will refer to many modules detailed further in the :ref:`modules` section.
Feel free to jump back and forth. The best way to understand these features is to consult
the 'opsmop-demo' feature on GitHub, and also as you read through :ref:`modules`, you will
see some of these features used in the examples in context.

.. _method:

Provider Selection
==================

Often, a *Type* may be coded to return a default *Provider* on a specific platform, but this is always
overrideable, either with one of the providers that ship with OpsMop or your own. To install a package
using the default *Provider*, we don't have to do anything special:

.. code-block:: python

    def resources(self):
        return Resources(
            Package(name="cowsay")
        )


This would usually select "yum", "apt", or "brew" on CentOS, Ubuntu, or OS X, repectively.

To specify or force a specific provider::

.. code-block:: python
    
    def resources(self):
        return Resources(
            Package(name="cowsay", method="yum")
        )

To specify a provider OpsMop doesn't know about, it's still possible to select one out of tree::

.. code-block:: python

    Package(name="cowsay", method="your.custom.provider.spork")

Expressing that full path is verbose, so it helps to save those strings to a python constant.

.. code-block:: python
    
    Package(name="cowsay", method=SPORK)

.. note:

    OpsMop is very new so providers will be growing rapidly for modules.  These are a great
    first area for contributions if you have needs for one.  See :ref:`development`.

.. _scoping:

Variable Scoping
================

We've already talked a little bit about variables, and knowledge of variables weighs in on
future sections.  OpsMop has a very simple to understand variable system based on the
concept of scope.  Variables defined at outer scopes are always available further
down, but changing a variable inside a scope does not effect the value at the outer scope.

In the opsmop-demo repository, `var_scoping.py <https://github.com/vespene-io/opsmop-demo/blob/master/content/var_scoping.py>`_ demonstrates
the various variable scopes in OpsMop. 

.. _templates:

Templates
=========

The :ref:`scoping` shows that variables can be set in many places.
Templates take those variables and inject them into strings.

OpsMop uses Jinja2 for templating, which is a powerful templating language that has quite a few capabilities
beyond simple substitution, conditions, and loops.

Because we prefer being explicit and predictable, OpsMop does not automatically template every string.

Only a few certain utility modules automatically assume their inputs are templates. One is :ref:`module_echo`:

.. code-block:: python

    Echo("My name is {{ name }}")

To explictly template a string for some other parameter, we use 'T()':

.. code-block:: python

    Package(name="foo", version=T("{{ major }}.{{ minor }}"))

The value "T" is a late binding indication that the value should be templated just
before check-or-apply mode application. Any variable in the current scope is available to 'T()'.
However, python variables are not.  To make them available to OpsMop you would need to do:

.. code-block:: python

    Set(foo_version=foo_version),
    Package(name="foo", version=foo_version)

.. note::
    Use of an undefined variable in a template will intentionally cause an error.

.. note::
    Because template expressions are late binding, they will push some type-checking that would
    normally happen before check-and-apply stages to runtime evaluation. For example, if this
    file was missing, it might not be determined until halfway through the evaluation of a policy::

        File(name="/etc/foo.cfg", from_file=T("content/{{ platform }}.cfg"))

    However, if the path was not evaluated with T(""), the fact that the file was missing
    could be detected far earlier.  Usage of :ref:`conditionals` instead of templated file
    paths may be preferable to keep the type checking features of OpsMop fully in play.

.. _eval:

Eval
====

Similar to T(), a computation of two variables is doable with Eval::

.. code-block:: python

    Echo(Eval("a + b"))

The difference with Eval() vs "T()" is that Eval can return native python types, whereas T() always
returns a string.  Here is a contrived example::

    Set(a=2, b=3),
    Set(c=Eval('a+b')),
    Debug(a, b, c)
   
.. note::
    Eval is quite useful with :ref:`conditions`, described below.

.. _conditions:

Conditions
==========

Any role, policy, or resource can be given a conditional.  If the conditional is true, that resource
and resources therein will be skipped during the check or apply phase.

Expressions are specified with "when=", which accepts legal Jinja2 expressions.  This is technically
implemented using Eval() but leaving off Eval is provided as syntactic sugar::

.. code-block:: python

    Shell("reboot", when="a > b")


This is the same as the overly redundant::

.. code-block:: python

    Shell("reboot", when=Eval("a > b"))


And while it serves no purpose that couldn't be achieved with a comment, technically this also disables
a resource::

.. code-block:: python

    Shell("reboot", when=False)

.. note::
    Development info: Both Eval() and T() are implementations of the class "Deferred", and you can write your own
    subclasses of Deferred if you wish to write any kind of runtime lookup into an external system.
    See :ref:`plugin_development`.

.. note::
    Referencing an undefined variable in a condition will intentionally result in an error.

.. _nested:

Nested Scopes
=============

Nested Scopes were created for quickly attaching a condition to a large number of resources::

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
demoed in `var_scoping <https://github.com/vespene-io/opsmop-demo/blob/master/content/var_scoping.py>`_.

.. _facts:

Facts
=====

Facts are information about the system, including information like the OS version and architecture,
that are discovered by OpsMop dynamically at runtime.  

.. note:

    The facts implementation of OpsMop uses on-demand memoization, so the cost of computing an expensive 
    fact will not be realized unless it is actually referenced.

Facts are accessed by using the "F" accessor in the policy language, and can be used anywhere::

.. code-block:: python

    Echo("The OS type is {{ F.os_type }}")


Or more simply::

.. code-block:: python

    Echo(F.os_type)


Here is a conditional::

.. code-block:: python

	Echo("I am Linux", when=F.is_linux)


For a full list of available facts see :ref:`facts_list`.

.. note:

   Referencing a fact that doesn't exist will cause an error.

.. note:

   At this time you can create your own facts by subclassing ospmop.core.facts.F.  Keep in mind that the development implementation
   for templates, however, does *NOT* allow injection of your own Facts into the template engine. To work around this, you can
   register your fact with Set() to store it in the variable namespace.

.. _registration:

Registration
============

The value of one command may be saved and fed into the output of another. 

This value is entered into local scope, and can be saved into global scope using SetGlobal(), 
which is described in a later chapter::

.. code-block:: python

    def resources(self):
        return Resources(
            Shell('date', register='date'),
            Debug('date'),
            Echo("{{ date.rc }}"),
            Echo("{{ date.data }})
        )


.. note:
    Using Echo to show templates on the screen is a useful debug technique, but the :ref:`module_debug` module is often easier.

Registration works well with :ref:`conditions`, :ref:`failed_when` and :ref:`changed_when`

.. note:
    Depending on resource, the value "rc" or "data" may be None. Register is most commonly
    used with shell commands. Providing methods on the returned result to provide
    access to the 'changed or not' status may occur in a later version.

.. _ignore_errors:

Ignore Errors
=============

Most commands will intentionally stop the execution of an OpsMop policy upon hitting an error. A common
example would be Shell() return codes. This is avoidable, and quite useful in combination with the register
command.

.. code-block:: python

    def resources(self):
        return Resources(
            Shell("ls foo | wc -l", register="line_count", ignore_errors=True),
            Echo("line_count.data")    
        )


.. _changed_when:

Change Reporting Control
========================

NOTE: pending feature - this feature will be released shortly.

A resource will mark itself as containing changes if it performs any actions to the system.
Sometimes, particularly for shell commands, this is not appropriate. The state can
be overriden as follows:

.. code-block:: python

    Shell("/bin/foo --args", register="x", ignore_errors=True, changed_when="x.rc == 1", notify="some_step")


If not using handlers, the change reporting isn't too significant, but it will affect CLI output counts at
the end of the policy execution.

.. _failed_when

Failure Status Overrides
========================

NOTE: pending feature - this feature will be released shortly.

By default if a command returns a fatal error, the program will halt at this step.  The 'ignore_errors'
mentioned above is technically equivalent to::

.. code-block:: python
    
    Shell("/bin/foo --args", register="x", failed_when=False)


However, that's a weird example! In a more practical example, suppose we have a shell command that
is programmed incorrectly and returns 5 on success::

.. code-block:: python

    Shell("/bin/foo --args", register="x", failed_when="x.rc != 5")


Ok, that's ALSO a weird example.  What if we have a shell command that we should consider failed
if it doesn't contain the word "SUCCESS" in the output?  Easy::

.. code-block:: python
    
    Shell("/bin/foo --args", register="x", failed_when="x.data.find('SUCCESS') == -1")


Find in the above example is a Python method available on string objects, and x.data contains the
output of any shell command.

If you find it clearer to read, remember you can assign a conditional test to a variable::

.. code-block:: python

    Shell("/bin/foo --args", register="x", failed_when=SUCCESS_IN_OUTPUT)


.. _signals:

Signals
=======

Handler objects, described above, are resources that only activate when another resource reports having
changed the system. Resources mark change any time they fulfill an action that they have planned.

.. code-block:: python

	File("/etc/foo.conf", from_template="templates/foo.conf.j2", signals="restart foo app")


Signals will cause the corresponding handler to fire, for instance, if the Role defines some handlers 
like so::

.. code-block:: python

    def set_handlers(self):
        return Handlers(
           restart_foo_app = Service(name="foo", restarted=True) 
        )


Then the restart command would only one if some resource with the designated 'signals' parameter
indicated some change was neccessary. In the above example, if the configuration file already had
the correct contents, it would not request a restart of the service.

Next Steps
==========

* :ref:`modules`
* :ref:`plugin_development`
* :ref:`api`


