.. image:: opsmop.png
   :alt: OpsMop Logo

About OpsMop
------------

OpsMop is a agentless distributed SSH control plane for all manner of computing tasks, created and led by 
`Michael DeHaan <http://michaeldehaan.net>`_.

OpsMop works off a static or dynamic inventory of systems, and then allows running
arbitrary tasks, represented by Python functions, against those systems. Any library 
dependencies are transferred automatically, and reports are provided on a host by host basis of successes and failures. 
Callbacks are pluggable, allowing for easy injection of results into external software systems. 

OpsMop allows for addressing different tiers of machines at different orders, including controls 
over how many instances to address at once.  Modelling of complex orchestration behaviors, including rolling updates involving 
load balancers, is also trivial.  Further, multiple-levels of bastion hosts are supported, allowing for highly-efficient fanout topologies.

While not limited to declarative host configuration, OpsMop also includes a strong model-based class library, that can be easily
mixed in with standard Python functions.  Common industry features such as installing packages, file transfer, templates, and starting
OS services are supported without requiring installation of any permament management agents.

Most tools in this space are built around particular use cases related to systems configuration.  Instead, OpsMop allows for full programmability, 
so it can easily interact with arbitrary software systems at any point in time, rather than constraining the user along particular language
and use-case guiderails. Use cases are not limited to configuration or application deployment, but can be completely open ended.  While not designed
for a particular audience, OpsMop is especiallly appropriate within large and distributed datacenter environments, particularly in verticals such as 
finance, renderfarm, IOT, or edge computing.

Operating Systems
=================

Supported control platforms and targets:

* Linux
* BSD
* OS X

Status
======

Beta. 

Share language feedback, thoughts, and experiences on the `forum <https://talk.msphere.io>`_.

See also: :ref:`development` and :ref:`community`

License
=======

* Apache2

GitHub
======

* `opsmop <http://github.com/opsmop/opsmop>`_
* `opsmop-demo (examples) <http://github.com/opsmop/opsmop-demo>`_

Forum
=====

* `Join here <https://talk.msphere.io/>`_

Twitter
=======

* `@opsmop <https://twitter.com/opsmop>`_

Support and Engineering Contracts Available
===========================================

Please contact <mailto:michael@michaeldehaan.net>Michael DeHaan</A> for details.