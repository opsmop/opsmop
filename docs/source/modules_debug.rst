Assert
------

The assert module raises errors when various checks do not pass.

Parameters
==========

Assert takes no specific parameters.

Examples
========

A basic check::

    Assert(x=2, y=3, z="asdf")

Evaluation checks are also permissable::

    Assert(Eval("5000 - b > 200"))

You can also test against the truthiness of Facts::

    Assert(F.fact_name)

