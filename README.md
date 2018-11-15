OpsMop
======

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

Bugs
====

The bug tracker will open around December 1st.

API
===

The command line tool is only a small focus of this project. See opsmop.core.api for the code behind the command line.

Resource Acceptance
===================

In general, I want OpsMop to only have about 30-50 well-written core resources *TOPS* (types, not providers, providers
have no cap).  Some resources like services and packages may have 10 or so implementations for different platforms.

To control sprawl, where possible, our resources have multiple capabilities. For instance to add support to download files from the internet, this would go into the "file" module, rather than adding another module that was verb based like "curl".  Similarly,
"file" already does templates.

Where tools have easy command line equivalents we may encourage continued use of
those command line tools. Yum update? Just shell out to yum update.

Similarly, where command lines are strong ways to implement a provider, we use those, to keep code simpler,
more reliable, and less fragile than using a wide set of dependencies.

We generally like to see provider code implementations be VERY short, often relying on helper classes
added to opsmop.core.*, which is how things like templating code is standardized.

When reviewing resource code, pay special note to .plan("action"), .should("action"), and .do("action").

Plan says something is going to be done, should checks if it should be done, and then do does it. Doing
an action that is not planned, or planning an action and not doing it cause very useful errors.

These three methods are part of the well-split plan and execution model in OpsMop, which not only
allows for a very strong dry-run mode, but also error checking if a provider fails to perform an action
that it decided to do.

This will be covered in the upcoming plugin development guide.

License
=======

Apache 2

Author
======

Opsmop is written by Michael DeHaan.

(C) Michael DeHaan LLC, <michael@michaeldehaan.net>, 2018



