.. _local:

Local
-----

The easiest mode of opsmop to use is the local mode.

Opsmop uses policy files written in a pure-Python DSL.

See also :ref:`language`.

.. _validate:

Validate Mode
=============

Validate checks a policy file for syntax, parameters of invalid types, and missing files::

   opsmop validate path/filename.py

If you checked out the :ref:`demo` policy::

   opsmop validate opsmop-demo/content/filename.py

.. _check:

Check Mode
==========

Check mode runs a policy and reports on actions that should be changed, but does not
make any changes.  This is often called a 'dry-run' mode, and it is a first-class
citizen of OpsMop::

   opsmop check opsmop-demo/content/hello.py

.. _apply:

Apply Mode
==========

Apply mode runs a policy, plans what changes are needed, and also enacts those changes.
It is an error when the actions taken do not match the plan::

   opsmop apply opsmop-demo/content/hello.py

Next Steps
==========

See :ref:`language`



