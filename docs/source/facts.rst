.. _facts:

Facts
-----

Facts are truths about the system where OpsMop is being run, and are essentially like variables.  They can
be used in conditionals and functions.

An executable demo of facts is coming soon in the 'opsmop-demo' repo.

Some Examples
=============

Facts are accessed by using the "F" accessor in the policy language, and can be used anywhere.
The following demos are complimentary with the :ref:`advanced` language guide.

.. code-block:: python

    Echo("The OS type is {{ F.os_type }}")

Or more simply:

.. code-block:: python

    Echo(F.os_type)

Here is a conditional:

.. code-block:: python

	Echo("I am Linux", when=F.is_linux)

Or inside a Jinja2 template using the :ref:`module_file`:

.. code-block:

    I am {{ F.os_type }}

List of Available Facts
=======================

This area is in rapid development. Coming soon

Custom Facts
============

While you cannot create your own facts per se, a custom '/etc/opsmop/facts.d' feature will be provided in the near
future. Once complete, each file in 'facts.d' will be loaded into a fact value, accessible as::

    F.site_facts('factname')

This will then look for a file /etc/opsmop/facts.d/factname

If the fact is valid JSON or YAML, it will be returned as a complex data structure.  If the fact is an executable
file, the response from that file will be interepreted as JSON.  Otherwise, the value will be returned as a string.

In this way, facts can be implemented in any language.

.. _note:
   Cloud Tip! It may be tempting to write a fact that asks AWS for instance tags, but if you are in a truly immutable
   system, you can also just bake /etc/opsmop/site.d/ facts into your images, which is faster and will not
   hit any rate caps. You can then write policy that is conditional on what your images are, without querying the
   cloud to ask.

Want To Add New Facts?
======================

Contribution of new facts (particularly OS/hardware related facts) to the main fact code is quite welcome.  
See :ref:`development`. Thank you!



