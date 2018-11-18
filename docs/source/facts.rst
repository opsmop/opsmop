.. image:: opsmop.png
   :alt: OpsMop Logo

.. _facts:

Facts
-----

Facts are truths about the system where OpsMop is being run, and are usable in templates and conditionals.  
To view most of the available facts and their values, see :ref:`module_debug_facts`, though a listing of available facts
is also included below.

Alternatively from the shell::

     python -m opsmop.facts.facts

List of Available Facts
=======================

More facts will be added frequently.

.. list-table::
   :header-rows: 1

   * - Name
     - Description
   * - choice(a,b,c,d,e)
     - randomly returns one of the parameters. Useful for chaos.
   * - default_package_provider()
     - used internally by the Package type
   * - default_service_provider()
     - used internally by the Package type
   * - random()
     - returns a float between 0 and 1. Useful for chaos.
   * - release()
     - from `python's platform module <https://docs.python.org/3/library/platform.html>`_
   * - system()
     - from `python's platform module <https://docs.python.org/3/library/platform.html>`_
   * - version()
     - from `python's platform module <https://docs.python.org/3/library/platform.html>`_

It is possible not all facts are documented, always run the :ref:`module_debug_facts` example to check the facts available
on your platform. Again please remember that facts that take parameters, such as 'choice', do not appear in the DebugFacts
output.

Fact Examples
=============

Facts are accessed by calling functions on the instance variable "Facts", like "Facts.foo()", and can be used anywhere.

The following demos are complimentary with the :ref:`advanced` language guide.

.. code-block:: python

    def set_resources(self):
        return Resources(
            Echo("The OS type is {{ Facts.system() }}")
        )

Or more simply:

.. code-block:: python

    def set_resources(self):
        return Resources(
            Echo(Facts.system())
        )

Or just to use the DebugFacts module and print them out:

.. code-block:: python

    def set_resources(self):
        return Resources(
            DebugFacts()
        )

To use a Fact in a conditional:

.. code-block:: python

	Echo("Not Darwin", when=(Facts.system() != "Darwin"))

Or inside a Jinja2 template, anywhere in OpsMop, you can also use Facts as you would expect:

.. code-block:

    I am {{ Facts.system() }}


Custom Facts
============

While you cannot create your own facts per se, a custom '/etc/opsmop/facts.d' feature will be provided in the near
future. Once complete, each file in 'facts.d' will be loaded into a fact value, accessible as::

    F.site_facts('factname')

This will then look for a file /etc/opsmop/facts.d/factname

If the fact is valid JSON or YAML, it will be returned as a complex data structure.  If the fact is an executable
file, the response from that file will be interepreted as JSON.  Otherwise, the value will be returned as a string.

In this way, facts can be implemented in any language.

.. note:
   Cloud Tip! It may be tempting to write a fact that asks AWS for instance tags, but if you are in a truly immutable
   system, you can also just bake /etc/opsmop/site.d/ facts into your images, which is faster and will not
   hit any rate caps. You can then write policy that is conditional on what your images are, without querying the
   cloud to ask.

Want To Add New Facts?
======================

Contribution of new facts (particularly OS/hardware related facts) to the main fact code is quite welcome.  
See :ref:`development`. Thank you!



