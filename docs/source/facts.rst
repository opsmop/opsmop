Facts
=====

Facts in OpsMop are accessed by using the "F.is_linux" convention mentioned in :ref:`advanced`.

Here is a list of all included Facts and some examples of possible values::

(THIS SECTION UNDER CONSTRUCTION - SOON).

Custom Facts
============

While you cannot create your own facts, a custom '/etc/opsmop/facts.d' feature will be provided in the near
future. Once complete, each file in 'facts.d' will be loaded into a fact value, accessible as::

    F.site('fact')

If the fact is valid JSON or YAML, it will be returned as a complex data structure.  If the fact is an executable
file, the response from that file will be interepreted as JSON.

New Facts?
==========

Contribution of new facts (particularly OS/hardware related facts) to the main fact code is quite welcome.  See :ref:`development_guide`


