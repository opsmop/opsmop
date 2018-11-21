.. image:: opsmop.png
   :alt: OpsMop Logo

.. _api:

API
===

This section describes the 'top-end' API for opsmop.  As opsmop is a Python subsystem, all of
the various classes could also be thought of as 'API', and for more information about
development on those, see :ref:`development`.

OpsMop is decidely API driven.  The CLI itself is a fully pluggable instantiation of the local API,
using a custom callback class.

As OpsMop grows, :ref:`pull` and :ref:`push` features will also have strong API support.

It is probably easiest to simply refer to GitHub to start:

* `api.py <https://github.com/opsmop/opsmop/blob/master/opsmop/core/api.py>`_
* `cli.py <https://github.com/opsmop/opsmop/blob/master/opsmop/client/cli.py>`_
* `callbacks <https://github.com/opsmop/opsmop/blob/master/opsmop/client/callbacks.py>`_
* `bin/opsmop <https://github.com/opsmop/opsmop/blob/master/bin/opsmop>`_

From the above links, you should see it is quickly easy to customize the output of the system as well as write
your new applications.

See Also
--------
* :ref:`development`
