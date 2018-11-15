OpsMop
======

(Fair warning: FULL DOC SITE COMING THIS WEEKEND - this Readme may not be 100% accurate!)

OpsMop is a next-generation configuration management platform from Michael DeHaan, focused on web-scale deployments, extremely maintainable high-quality plugins, and ease of use through a Python 3 DSL.

OpsMop is currently an alpha level codebase in very active development, currently offering a limited set of supported
modules.

Local support is available today, pull support will be added in approximately 1-month.  Development to date has prioritized
working on the language, and by December 1st we should have stable implementations for about 10 modules, across CentOS
and Debian.

At this point, this project is in language feedback stage. We will be wide open for pull requests of all kinds starting
around December 1.

In the meantime, I would *LOVE* to have your feedback and wish list and ideas on the OpsMop forum of http://talk.vespene.io/.
You can also send me a direct message at @laserllama on twitter, or email me at michael@michaeldehaan.net if you would
like to share more info than you normally could on a public forum. It's 2018, what do you want in a configuration tool?

Language Examples
=================

Sample content for opsmop is available in the demo repository:

   [opsmop-demo](https://github.com/vespene-io/opsmop-demo)

How To Review What's Here
=========================

See the opsmop-demo repo above.

At the moment there is no PyPi package.

You will either need a python3 virtualenv, and then do "make requirements" to install packages:

    git clone https://github.com/vespene-io/opsmop.git
    cd opsmop
    virtualenv env -p /usr/local/bin/python3
    make requirements

You will also want to check out the example content into a different directory:

    https://github.com/vespene-io/opsmop-demo.git
   
To run the examples:

    opsmop check opsmop-demo/content/<filename>.py
    opsmop apply opsmop-demo/content/<filename>.py

The application will CD into the path specified, so all paths referenced in
the OpsMop policy will be relative to there.

To look at modules to see how easy it is to write a module, I recommend looking at modules
like 'service' (brew implemented, quickly), 'package' (also just brew ATM), and 'shell'.

Available Types for OpsMop Language Files
=========================================

See opsmop/resources/*.py for the methods they take.  
See demo/*.py for example usage.

* Set - sets runtime variables
* File - copies files or templates, sets modes, etc
* Echo - prints debug or informational messages
* Shell - runs shell commands, either from files or just by strings
* Service - starts and enables services, disables, etc - currently a rough brew example only
* Package - installs or upgrades packages - currently a rough brew example only

This is very minimal.  Our near-term next steps will be to fill out the service and package
management modules.  

yum, apt for package and systemd for service will come first.

Once we're happy with *one* implementation in each category for package and service,
pull requests will be opened up for everything, including entirely new types of resources.

The goal is for all modules to serve as very strong examples for future modules before
we get going too fast.

Extensive module documentation with examples will be added very soon.

Templates
=========

Any string in an OpsMop policy can be a template, and of course from_template
in the File module also loads templates.

Templates are evaluated with Jinja2.

Only OpsMop variables and facts are available in templates at this time.

See the "V.x" and "F.x" type examples in demo/content.py

Additional modifications to allow access to the Python scope may be added later.

Facts
=====

Facts are variables about the OS for use in templates.

OpsMop has a facts system, see demo/conditionals.py and opsmop/client/facts.py

The facts are based on memoized functions where expensive facts are calculated only
once the first time they are accessed, leading to an extremely responsive experience.

This means there is no reason to disable fact evaluation.

Deferreds
==========

As demoed in demo/conditionals.py, OpsMop has a very sophisticated conditional evaluation
system, that calculates as much as possible at load time, but still has options for
runtime evaluation.

Deferreds can easily access external resources of all kinds, possibly including
remotely managed feature flag gates!

Bugs
====

The bug tracker will open around December 1st.

API
===

The command line tool is only a small focus of this project. See opsmop.core.api for the code behind the command line.

License
=======

Apache 2

Author
======

Opsmop is written by Michael DeHaan.

(C) Michael DeHaan LLC, <michael@michaeldehaan.net>, 2018



