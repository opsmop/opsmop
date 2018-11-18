.. image:: opsmop.png
   :alt: OpsMop Logo

.. _development:

Development Guide
-----------------

There are lots of ways to customize OpsMop - especially so because the language is all Python.  You might also want to add some changes upstream.
This guide will hopefully help you out in that quest! If you have any development questions, you are also welcome to stop by the :ref:`forum`.

.. _new_providers:

Adding New Providers
====================

Suppose you wanted to make opsmop be able to install a new kind of package or handle a new OS init system.  To do this, you would
need to implement a new provider.

All providers extend from opsmop.types.provider.Provider.

The best provider to copy when writing your own provider would be looking at the providers for
 :ref:`module_shell` or :ref:`module_package` - they are both simple and illustrative.

See :ref:`method` for how to pick a provider inside  your policy file, rather than relying on the default.  By supplying the method
parameter, you can easily attach any provider class to an existing type.

Should you want to make your new provider the default for a particular OS though, that requires a tiny amount more work -
subclassing the Type itself.  (See :ref:`new_types`)

If you just want to add new parameters to support a new provider you are adding, it is usually acceptable to add those parameters
to the Type itself - and if you are adding a new provider via a github pull request, it naturally makes sense that you would
also edit the Type() code to surface any new parameters.

.. _new_types:

Writing New Types
=================

All types extend from `opsmop.types.type.Type <https://github.com/vespene-io/opsmop/blob/master/opsmop/types/type.py>`_

The best type to copy when writing your own type would be :ref:`module_shell` or :ref:`module_package`.

If you want to find an example of a type that supports default providers for different platforms, and also allows the user to select
their own types, we recommend :ref:`module_package` or :ref:`module_service`.

If writing new types, you will need to import these types into your policy file. The "easy.py" shortcut shown in most examples in the 'opsmop-demo' directory
only import this one file.

Once again, if you're wishing to contribute a new provider, and it requires a new parameter, please include both in the same pull request.

.. _custom_facts:

Adding Custom Facts
===================

The code for facts (see :ref:`facts`) is in `opsmop.facts.facts.Fact <https://github.com/vespene-io/opsmop/blob/master/opsmop/facts/facts.py>`_

If you write your own fact classes, you should make it available to template namespace by calling set::

.. code-block:: python

    def set_resources(self):
        return Resources(
             # ...
             Set(site_facts=AcmeLabsCustomFacts())
             # ...
        )


A future feature for custom facts in /etc/opsmop/facts.d is also pending development, which will allow string, JSON, or YAML facts as well as executable
facts to be written in any language. See :ref:`facts`

.. _lookups:

Adding Custom Lookups
=====================

Lookup Values are subclasses of `opsmop.lookups.Lookup <https://github.com/vespene-io/opsmop/blob/master/opsmop/lookups/lookup.py>`_, and are functions 
that are lazy-evaluated at check or apply stage.  Ok, it's not exactly true they are functions. They are black-magic metaclass stuff. But eventually
they are functions!

They are also easy to write, and you don't need to know anything about Python metaclasses to do it.

Take a look at any of the subclasses in the 'opsmop.lookups' directory.

Examples of core Lookups include Eval() for string evaluation and T() for :ref:`templates`.

An example of a future custom type might be a 'Etcd' or 'Consul' or even DNS record lookup plugin - and something like this would be something we'd gladly include in
the core distribution (probably then creating an opsmop.lookups package).

Such a plugin could (and probably should) also memoize the value to prevent repeated computations.

A quick reminder, lookups aren't automatically available inside Jinja2, and to do that, use set::

.. code-block:: python
    def set_resources(self):
        return Resources(
             # ...
             set(ff01=CustomFeatureFlagLookup('ff01'))
             # ..
        )

.. _callbacks:

Custom Callbacks
================

CLI output is driven by a callback plugin, as shown in `opsmop.client.callbacks <https://github.com/vespene-io/opsmop/blob/master/opsmop/client/callbacks.py>`_.

You can easily customize OpsMop by replacing it with another plugin, potentially a subclass.

Using a new callback would require subclassing cli.py and a new bin/opsmop, which is just a thin layer over cli.py
We can easily consider reading the callback name from an environment variable or a CLI parameter as a feature upgrade.

Future plans for :ref:`pull` and :ref:`push will also feature different types of callback classes or additional callbacks.

.. _roadmap:

Roadmap
=======

While OpsMop has a fluid roadmap, at this stage of development TODO.md is illustrative of some near-term features.
We want the best ideas at the moment to win, and a lot of our development time will also be devoted to shepherding
incoming pull requests and ideas from folks like yourself.

If you have questions (or would like to help with something specific, stop by the :ref:`forum`.

See Also
========
* :ref:`api`
* :ref:`community`


