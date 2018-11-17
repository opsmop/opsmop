.. _facts:

Facts
-----

Facts are truths about the system where OpsMop is being run, and are essentially like variables.  They can
be used in conditionals and functions.

An executable demo of facts is coming soon in the 'opsmop-demo' repo.

Facts in OpsMop are accessed by using the "F.is_linux" convention mentioned in :ref:`advanced`.
For instance, from within a Jinja2 template::

    My OS is {{ F.os_type() }}

List of Facts
=============

Coming soon

Custom Facts
============

While you cannot create your own facts per se, a custom '/etc/opsmop/facts.d' feature will be provided in the near
future. Once complete, each file in 'facts.d' will be loaded into a fact value, accessible as::

    F.site_facts('factname')

This will then look for a file /etc/opsmop/facts.d/factname

If the fact is valid JSON or YAML, it will be returned as a complex data structure.  If the fact is an executable
file, the response from that file will be interepreted as JSON.  Otherwise, the value will be returned as a string.

Want To Add New Facts?
======================

Contribution of new facts (particularly OS/hardware related facts) to the main fact code is quite welcome.  
See :ref:`development_guide`. Thank you!



