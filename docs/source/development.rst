.. _development:

Development Guide
-----------------

There are lots of ways to customize OpsMop.  This guide will discuss some customizations that you wish to make at your own site
and not distribute, as well as other ways where you might wish to contribute back to OpsMop with a pull request.

.. _new_providers

Adding New Providers
====================

All providers extend from <LINK>.

<CODE EXAMPLE>

The best provider to copy when writing your own provider would be <LINK TO SHELL> or <LINK TO PACKAGE>.

See :ref:`method` for how to use an existing type but request it be fulfilled by your own provider implementation.
If you need to add extra parameters you will possibly want to write your own new type and use that in your policy
file instead of the stock ones loaded by "easy.py".

However, if adding a new provider of general interest via pull request to our GitHub, it is usually acceptable
to add new arguments - though we'll probably want to discuss what they should be to avoid too many provider
specific arguments.

If a provider recieves arguments it does not understand it should use "self.error()" to fail the execution. In the near
future we may add a method to the provider for it to pre-validate some arguments during the validaton stage instead of waiting
until the check stage.

.. _new_types:

Writing New Types
=================

All types extend from <LINK>

<CODE EXAMPLE>

The best type to copy when writing your own type would be the <LINK TO SHELL>.

If you want to find an example of a type that supports default providers for different platforms, and also allows the user to select
their own types, we recommend <LINK TO PACKAGE>.

You will need to import these types into your policy file. The "easy.py" shortcut shown in most examples in the 'opsmop-demo' directory
only import this one file.

.. _custom_facts:

Adding Custom Facts
===================

The code for facts lives in <LINK>

The facts accessed by the Deferred Lookup "F" can be supplemented by writing your own lookup class, per :ref:`lookups`. Unfortunately
those custom facts cannot be easily injected into the template namespace.

A future feature for custom facts in /etc/opsmop/facts.d is pending development, which will allow JSON facts as well as executable
facts to be written in any language.

For instance, it would be trivial to write a fact that returns AWS tags, and then use those tags in OpsMop conditions.

.. _lookups:

Adding Custom Deferred Lookups
==============================

Deferred Values are subclasses of <LINK>.

Examples of core Deferred Lookups include Eval() and T() for :ref:`templates`.

Each statement can be passed to numerous values and is not evaluated until the provider "check" stage, allowing access to full
variable scopes.

An example of a custom type might be a 'Etcd' lookup plugin - and something like this would be something we'd gladly include in
the core distribution (probably then creating an opsmop.lookups package).

Custom Callbacks
================

CLI output is driven by a callback plugin, <HERE>.

This plugin is currently not user replaceable without writing a new copy of <LINK TO cli.py> and bin/opsmop but we can easily
consider reading the callback name from an environment variable.

Other Extensibility
===================

Additionally, when :ref:`push` and :ref:`pull` are implemented, these features will be implemented by mutliple different
types of plugins, for flexibility in storage, transport, output, and reporting.




