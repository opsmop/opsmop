OpsMop
======

OpsMop is a next-generation configuration management platform from Michael DeHaan.

It is focused on web-scale deployments, extremely maintainable high-quality plugins, 
and ease of use.

OpsMops configurations are written in a Python 3 DSL.

This is currently an alpha level codebase in very active development, currently offering a limited set of supported
modules and no remote features at this time.

This project is in language feedback stage. Even the bug tracker is closed,
but there is a feedback forum open at talk.vespene.io for those who like
where this project might be headed.

In the coming weeks, the included providers will be polished up, along with APIs, and we'll start taking pull requests.

In the meantime, I would *LOVE* to have your feedback and wish list and ideas on the OpsMop forum of http://talk.vespene.io/.
You can also send me a direct message at @laserllama on twitter, or email me at michael@michaeldehaan.net if you would
like to share more info than you normally could on a public forum. It's 2018, what do you want in a configuration tool?

How To Review What's Here
=========================

To review opsmop, check out the code, then look at the language examples:
 
    vim demo/content.py (basics)
    vim demo/conditionals.py (advanced features)

You will either need a python3 virtualenv, and then do "make requirements" to install packages:

virtualenv env -p /usr/local/bin/python3
make requirements

Work on packaging and setup instructions will follow shortly.

To run the examples (Yes, You Can - There May Be Small Bugs):

    opsmop check demo/content.py
    opsmop apply demo/content.py

The application will CD into the path specified, so all paths referenced will be relative to there.
You can see we have a "files/" and "templates/" subdirectory in that same directory but there is no
enforced convention.

Fair warning: this CLI and output will probably change a lot.

The setup.py is also a work in progress, just run from the checkout for now.  You may need also
need to set PYTHONPATH so you can find opsmop when running straight out of checkout.

Feedback is particularly wanted on:

* Language design
* Type/provider APIs
* Feature ideas of absolutely all kinds - bring your wish list.

Areas that I know need total overhaul:

* Visitor and Executor and Callback code
* the file modules - these are just rough cuts

To look at modules to see how easy it is to write a module, I recommend looking at modules
like service (brew implemented, quickly), package, shell, echo, and so on.

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

Conditions
==========

As demoed in demo/conditionals.py, OpsMop has a very sophisticated conditional evaluation
system, that calculates as much as possible at load time, but still has options for
runtime evaluation.

Conditions can easily access external resources of all kinds, possibly including
remotely managed feature flag gates!

Bugs
====
There are probably LOTS right now, this is starting out of a rough cut with about four days of work
into it. The tracker will open up in a few weeks and we'll start smiting them.

API
===

While I like where it is going, the API is *NOT* ideal at the moment and will be cleaned up shortly. It is based on basic
generator code to walk a tree of resources, allowing different operations like "check"
and "apply" to be implemented using the same code.

All of these functions should be much cleaner and shorter.

We aim to have an *exceptionally* easy to use higher level API, and the CLI is not a good example of that just yet.

These classes thankfully already rely on a callback class implementation (this will change) that
makes it very easy to change the behavior of the program as well as basic output.  If you want to customize the output
or even send events to external systems, it is easy to do.

Subclassing Everything
======================

Because OpsMop is pure Python, rather than using an immediate language, 
everything is subclassable.

The most basic example is that you can write your own Types and Providers, but you can also
use existing types and still use your own implementations for them.

For instance, if you use a service manager called "SpaceCloud"...

When using basic types, it is possible to specify your own implementation in the policy, like
so:

   Package(name="foo", method="mypackage.provider.SpaceCloud")

To keep this clean, assign a variable to keep from retyping the package name.

You can then use any implementation you like, making for rapid development or customization
however you like.

All of this will be detailed in full in the future development guide.

Resource Acceptance
===================

In general, I want OpsMop to only have about 30-50 well-written core resources *TOPS*.  Some resources like services
and packages may have 10 or so implementations for different platforms.

To control sprawl, where possible, we include resource support into common code, using support classes to keep the main
applicaitons very clean, short, and where possible, generic.

For instance to add support to download files from the internet, this would go into the
"file" module, rather than adding another module that was verb based like "curl".

An existing example of that is the file module is also the copy/template module.
This keeps everything more easy to remember.

Where tools have easy command line equivalents we may encourage continued use of
those command line tools. Yum update? Just shell out to yum update.

Similarly, where command lines are strong ways to implement a provider, we use those, to keep code simpler,
more reliable, and less fragile.

We generally like to see provider code implementations be VERY short, often relying on helper classes
added to opsmop.core.*, which is how things like templating code is standardized.

When reviewing resource code, pay special note to .plan("action"), .should("action"), and .do("action").

Plan says something is going to be done, should checks if it should be done, and then do does it. Doing
an action that is not planned, or planning an action and not doing it cause very useful errors.

These three methods are part of the well-split plan and execution model in OpsMop, which not only
allows for a very strong dry-run mode, but also error checking if a provider fails to perform an action
that it decided to do.

Remote Functionality
====================

This POC is local only.  We'll discuss this on the forum shortly! I have some ideas but also want
to hear yours!

License
=======

GPL v3.

Author
======

Opsmop is written by Michael DeHaan.

(C) Michael DeHaan LLC, <michael@michaeldehaan.net>, 2018



