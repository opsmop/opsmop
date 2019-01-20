.. image:: opsmop.png
   :alt: OpsMop Logo

About OpsMop
------------

OpsMop is an extremely-efficient agentless distributed SSH control plane for all manner of computing tasks, created and led by 
`Michael DeHaan <http://michaeldehaan.net>`_.

OpsMop works off a (pluggable) inventory of systems/nodes, and then allows running
arbitrary tasks, represented by Python functions, against those systems. 

Any python dependencies used are transferred automatically, and reports are provided on a host by host basis of successes and failures.
Thanks to a clean API and pluggable callback classes, input from any external system, and output to other external systems is trivial.

While not limited to host configuration and application deployment, OpsMop also includes a strong model-based class library, that can be easily
mixed in with standard Python functions.  Common industry features such as installing packages, file transfer, templates, and starting
OS services are supported without requiring installation of any permament management agents.

OpsMop allows for addressing different tiers of machines at different orders, including controls 
over how many instances to address at once.  Modelling of complex orchestration behaviors, including rolling updates involving 
physical or cloud-based load balancers, is also trivial.  Further, multiple-levels of bastion hosts are supported, 
allowing for highly-efficient fanout topologies.

Most tools in this space are built around particular use cases related to systems configuration.  Instead, OpsMop allows for full programmability, 
so it can easily interact with arbitrary software systems at any point in time, rather than constraining the user along particular language
and use-case guide-rails. Use cases are not limited to configuration or application deployment, but can be completely open ended.  While not designed
for a particular audience, OpsMop is especiallly appropriate within large and distributed datacenter environments, particularly in verticals such as 
finance, render farms, retail installations, IOT, vending, telephony, and edge computing.

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