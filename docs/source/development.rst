.. image:: opsmop.png
   :alt: OpsMop Logo

.. _development:

Development Guide
-----------------

There are lots of ways to customize OpsMop.  You might also want to add some changes upstream.

This guide will discuss some customizations that you wish to make at your own site
and not distribute, as well as other ways where you might wish to contribute back to OpsMop with a pull request.

.. _new_providers:

Adding New Providers
====================

All providers extend from opsmop.types.provider.Provider.

The best provider to copy when writing your own provider would be looking at the providers for
 :ref:`module_shell` or :ref:`module_package` - they are both simple and illustrative.

See :ref:`method` for how to pick a provider inside  your policy file, rather than relying on the default.

If you need to add extra parameters to a type you will possibly want to write your own new type and use that in your policy
file instead of the stock ones loaded by "easy.py".

However, if adding a new provider of general interest via pull request to our GitHub, it is usually acceptable
to add new parameters - though we'll probably want to discuss what they should be to avoid too many provider
specific arguments.

.. _new_types:

Writing New Types
=================

All types extend from `opsmop.types.type.Type <https://github.com/vespene-io/opsmop/blob/master/opsmop/types/type.py>`_

The best type to copy when writing your own type would be :ref:`module_shell` or :ref:`module_package`.

If you want to find an example of a type that supports default providers for different platforms, and also allows the user to select
their own types, we recommend :ref:`module_package` or :ref:`module_service`.

If writing new types, you will need to import these types into your policy file. The "easy.py" shortcut shown in most examples in the 'opsmop-demo' directory
only import this one file.

.. _custom_facts:

Adding Custom Facts
===================

The code for facts (see :ref:`facts`) is in `opsmop.core.facts.Fact <https://github.com/vespene-io/opsmop/blob/master/opsmop/core/facts.py>`_

The facts accessed by the Deferred Lookup "F" can be supplemented by writing your own lookup class, per :ref:`lookups`. Unfortunately
those custom facts cannot be easily injected into the template namespace without first assigning them using :ref:`module_set`.

A future feature for custom facts in /etc/opsmop/facts.d is pending development, which will allow JSON facts as well as executable
facts to be written in any language.

.. _lookups:

Adding Custom Deferred Lookups
==============================

Deferred Values are subclasses of `opsmop.core.deferred.Deferred <https://github.com/vespene-io/opsmop/blob/master/opsmop/core/deferred.py>`_, and are functions that are lazy-evaluated at check or apply stage.

Examples of core Deferred Lookups include Eval() and T() for :ref:`templates`.

Each statement can be passed to numerous values and is not evaluated until the provider "check" stage, allowing access to full
variable scopes.

An example of a custom type might be a 'Etcd' or 'Consul' or even DNS record lookup plugin - and something like this would be something we'd gladly include in
the core distribution (probably then creating an opsmop.lookups package).

Such a deferred plugin could also memoize the value to prevent repeated inefficient computations.

.. _callbacks:

Custom Callbacks
================

CLI output is driven by a callback plugin, as shown in `ospmop.client.callbacks <https://github.com/vespene-io/opsmop/blob/master/opsmop/client/callbacks.py>`_.

This plugin is currently not user replaceable without writing a new version of cli.py and bin/opsmop but we can easily
consider reading the callback name from an environment variable as a feature upgrade.

Other Extensibility
===================

Additionally, when :ref:`push` and :ref:`pull` are implemented, these features will be implemented by mutliple different
types of plugins, for flexibility in storage, transport, output, and reporting.  More on these later!

.. _roadmap:

Roadmap
=======

While OpsMop has a fluid roadmap, at this stage of development TODO.md is illustrative of some near-term features.
If you have questions (or would like to help with something specific, stop by the forum!)

See Also
========
* :ref:`api`
* :ref:`community`


