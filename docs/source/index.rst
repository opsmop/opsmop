.. image:: opsmop.png
   :alt: OpsMop Logo

It's OpsMop!
------------

Cleanup on Datacenter Aisle 3!

OpsMop is a next-generation, no-compromise automation system from `Michael DeHaan <http://michaeldehaan.net>`_.

Uses
====

* Web-scale configuration management of all Linux/Unix systems
* Application deployment
* Immutable systems build definition
* Maintaining stateful services such as database and messaging platforms
* Automating one-off tasks & processes
* Deployment and management of the undercloud

Features
========

* Python 3 DSL
* Declarative resource model with imperative capabilities
* Type / Provider plugin seperation
* Implicit ordering (with handler notification)
* Formalized "Plan" vs "Apply" evaluation stages
* Early validation prior to runtime
* Programatically scoped variables
* Strong object-orientation

See :ref:`language` and :ref:`advanced`.

Run Modes
=========

* Seperate validate, check ("dry-run"), and apply modes
* :ref:`local`
* :ref:`pull` pluggable transports (soon)
* :ref:`push` configuration with multi-tier addressing (soon)
* All aim for exceptional runtime speed

Project Values
==============

* Minimalism
* Flexibility
* Language design
* Code quality
* Speed
* Applied Experience

Operating Systems
=================

Supported:

* Linux
* BSD
* OS X

Status
======

Alpha. OpsMop is in a tech-preview/feedback phase.

We are still refactoring some minor parts and working on plugins. Existing modules/plugins are limited
and features are not fully implemented in all cases. Still, the language itself is very well evolved
and close to complete. We love new ideas, so stop by the forum and share your ideas and to talk
about the things you want to configure with OpsMop. If you would like to get involved with development,
now is the time to read up on OpsMop, and the floodgates will be open in December!

See also: :ref:`development` and :ref:`community`

Schedule
========

* Open for pull requests and bug reports starting December 1.
* December will be devoted almost exclusively to plugin development, helping new contributors, and small language tweaks
* Pull mode likely debuts in December 2018.
* Documentated language features will be locked in and largely stable by January 2019
* First 'tagged' stable release in early Feburary 2019, but master branch usage is always encouraged

If you like where this is going, now is the time to join up with thoughts
and potentially code. Read over :ref:`community` and :ref:`development` for details 
and we would be glad to have you!

License
=======

* Apache2

GitHub
======

* `opsmop <http://github.com/opsmop/opsmop>`_
* `opsmop-demo (examples) <http://github.com/opsmop/opsmop-demo>`_

Forum
=====

* `Join here <https://talk.vespene.io/c/opsmop-general>`_

Twitter
=======

* `@opsmop <https://twitter.com/opsmop>`_

