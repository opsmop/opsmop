.. image:: opsmop.png
   :alt: OpsMop Logo

.. _local:

Local
-----

While most interest of ospmop will be around remote configuration (see :ref:`push`), the simplest way to use OpsMop to use is with the local command line. 

Opsmop uses policy files written in python.  The command line simply runs particular classes, called *Roles*, and runs them.

See :ref:`language` for more about the contents of those files.

.. _check:

Check Mode
==========

Check mode runs a policy and reports on actions that should be changed, but does not
make any changes (use :ref:`apply` to make changes).  This is often called a 'dry-run' mode, 
and dry-run support is a first-class citizen of OpsMop::

   cd opsmop-demo/content
   python3 hello.py --check --local

.. _validate:

Validate Mode
=============

To just look for missing files and bad parameters, without running the full check mode,
you can also run::

   cd opsmop-demo/content
   python3 hello.py --validate --local

.. _apply:

Apply Mode
==========

Apply mode runs a policy, plans what changes are needed, and also runs the policy::

    cd opsmop-demo/content
    python3 hello.py --apply --local

.. note:
    OpsMop enforces that planned actions reported in check mode
    match those ran in apply mode. This encourages all modules to have
    have well-implemented dry-run simulations.

Next Steps
==========

See :ref:`language`



