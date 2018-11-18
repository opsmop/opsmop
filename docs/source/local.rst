.. image:: opsmop.png
   :alt: OpsMop Logo

.. _local:

Local
-----

The easiest mode of opsmop to use is the local mode command line.  You could technically also use the :ref:`api`, and
soon there will also be :ref:`pull` and :ref:`push` modes. 

So, as mentioned elsewhere, Opsmop uses policy files written in a pure-Python DSL.  The command line simply
names that policy file and runs it.

(See also :ref:`language` for the contents of those files)

.. _validate:

Validate Mode
=============

Validate checks a policy file for syntax, parameters of invalid types, and missing files::

   opsmop validate path/filename.py

If you checked out the :ref:`opsmop-demo <https://github.com/vespene-io/opsmop-demo>`_ repo::

   opsmop validate opsmop-demo/content/filename.py

Any paths referenced in the policy file will be relative to the directory that executed policy file is in.

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



