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

All types extend from `opsmop.types.type.Type <https://github.com/opsmop/opsmop/blob/master/opsmop/types/type.py>`_

The best type to copy when writing your own type would be :ref:`module_shell` or :ref:`module_package`.

If you want to find an example of a type that supports default providers for different platforms, and also allows the user to select
their own types, we recommend :ref:`module_package` or :ref:`module_service`.

If writing new types, you will need to import these types into your policy file. The "easy.py" shortcut shown in most examples in the 'opsmop-demo' directory
only import this one file.

Once again, if you're wishing to contribute a new provider, and it requires a new parameter, please include both in the same pull request.

.. _custom_facts:

Adding Custom Facts
===================

The code for facts (see :ref:`facts`) is in `opsmop.facts.facts.Fact <https://github.com/opsmop/opsmop/blob/master/opsmop/facts/>`_ and they are just
simple classes that are made available to templates and regular python conditionals.

.. _callbacks:

Custom Callbacks
================

CLI output is driven by callback plugins, as shown in `opsmop.client.callbacks <https://github.com/opsmop/opsmop/blob/master/opsmop/callbacks/>`_.

You can easily customize OpsMop by replacing or augmenting callback plugins.

See Also
========
* :ref:`api`
* :ref:`community`


