.. image:: opsmop.png
   :alt: OpsMop Logo

Frequently Asked Questions
==========================

Some common questions

How Did You Get To Be So Awesome?
---------------------------------

Thanks, Mom!

How Is OpsMop Different From X?
-------------------------------

Ok, the one question I don't like.  You'll have to look for yourself.

OpsMop contains the features documentated on this web site. The other tool has features documented on the other tool web site. 
Some of the features are different or work differently!

You might like the language of one thing more than the other. Pick that thing.

If you like where we are going and want to hop on board, we'd love to have you.

Multiple Package Installs
-------------------------

Right now, the Package() resource doesn't batch package requests together.

When installing multiple packages, the package manager can often be slow (depending on the platform).  

For instance, imagine the following::

    Package(name="foo1", installed=True),
    Package(name="foo2", installed=True),
    Package(name="foo3", installed=True),
    Package(name="foo4", installed=True)

Each operation will typically start some new kind of transaction.  While we *COULD* handle it, it is important to realize
OpsMop strongly believes in pragmatism. It is unlikely you will need to signal for this event, so just do this::

    Shell("yum install -y foo1 foo2 foo3 foo4")

Easy enough.

The "name" parameter might take an array in the near future, but what's wrong with the shell command?  Nothing, really.

Are There Going To Be New Language Features?
--------------------------------------------

Yes, definitely!  Lots! However OpsMop strongly values backward compatibility, and will never let you down or hurt you.

If you have new ideas, see :ref:`community` and share your ideas on the forum. We would be glad to have them, and you
would like to maybe add them, that would also be great! OpsMop is designed to be a relatively easy to understand
codebase and we would love that.

If you have ideas for new language features, stop by the forum. See :ref:`community` for details.

Push vs Pull vs Local - What Does OpsMop Do?
--------------------------------------------

Right now, OpsMop is local only - but not for long.

Pull modes will come out next (soon), followed shortly thereafter by a powerful push-mode orchestrator
capable of multi-tier application in very specific orderings.

Eveything will be super configurable, rigorously engineered, and very fast.

Each will rely on opsmop and other tools in a stackable way and should be extremely pluggable, and also fast.

I Have A Develoment Question?
-----------------------------

Great! Thanks for the interest! Please check out :ref:`development`!  We would be glad to help you with pull requests, and also feel
free to stop by the forum listed on :ref:`community` with development questions.

How Do You See Modules Growing?
-------------------------------

In order to maintain an extremely high standard of quality, I would hope to see OpsMop stop at around 50 or so modules
in the core distribution. In some cases, modules may be merged.  Each module can have different provider implementations, and in
some cases like Package, I would not hold any limits to accepting modules for every language distribution (pip, npm, etc) on
providers, just types.

What we end up with is a toolbox that contains what is enough for 95% of the use cases out there, and allow the other 5%
to be performed easily, either by calling a script or using a custom non-tree module.

Just to ensure strong upkeep, we are unlikely to include modules that are difficult to test, including modules for paid services
that we do not use. However, the API remains fully extensible and does not block such efforts.

Where a command line tool exists and is already clear, sometimes we don't want a module. If something can be handled
by the :ref:`module_file`, that's the best way to configure something rather than maintaining custom code
designed to do in-place error-prone rearrangement on a configuration file.

An example of this is we don't need a "/sbin/reboot" module because there already is "/sbin/reboot".  Configuration tools
do serve to reduce our need to memorize a wide variety of Linux/Unix tools, but there is a balance to be struck. Often
CLI versions will be faster and have more stable APIs.

Another important aspect of OpsMop is we prefer to see some modules become robust and comprehensive versus splitting them into
too many sub-modules. For instance the file module contains the logic to template files, rather than having a seperate module
to do this.

Thus, with even 50 or so modules (not counting provider implementations) the feature set of OpsMop will still be incredibly
large.

Will You Integrate With (Other Config Tool)?
--------------------------------------------

OpsMop is about building no-compromise solutions, and we don't want to stay up to date with what other
players are doing. We believe in doing things differently. OpsMop should work instead to replace those other systems.
We are confident in our ability to move very fast and also develop very clean, stable, and well supported solutions.

As mentioned elsewhere, we do however not solve certain problems, such as cloud topology definition, and would
recommend other solutions (like CloudFormation or Terraform or python scripting with boto) in those cases.

Can You Write Modules In Any Language?
--------------------------------------

Nope! You have to use Python 3.

You could technically write a bridge module though, but it's not something we want for the core program, as we think
there is a very strong reason for everybody collaborating around using the same language.

OpsMop modules take advantage of a lot of features for code reuse.  We also minimize forking to
maintain execution speed.

This is to not say you couldn't invoke a shell script, or a program in some other language, and record the output
and return code, which you can still of course do, either. 

How Do I Do (Complicated Thing Without A Module)
------------------------------------------------

There really needs to be a Script module feature to make this easier soon, but if you don't feel like writing a type & provider, OpsMop can always
push a script::

    File(name="/opt/opsmop/", directory=True),
    File(name="/opt/opsmop/setup.sh", from_file="files/setup.sh"),
    Script("bash /opt/opsmop/setup.sh")

Just return 0 on success and non-zero on failure.

We should have that script module shortly!
  
Is There Going to be a community module or policy site?
-------------------------------------------------------

No. However if there are some really good community modules we don't want to maintain in core I can see a list of them
going up on the this documentation site as a bonus chapter with some minimal YMMV disclaimers.

What Platforms Does This Support?
---------------------------------

The system should run on any Unix system with Python 3.

My System Doesn't Have Python 3
-------------------------------

This is a good opportunity to prepare a new base image and use that base image for all of your projects.
The future push mode support may include some bootstrapping options.

Python 3 is great and worth it.

Are you going to do Windows?
----------------------------

Not really. I don't use Windows in any capacity, but I am open to making sure the core application (if not the types/providers)
do run on Python on that platform.  That would include using os.path.join() and so on. However, this project will not include
Windows specific modules in the main distribution (no powershell, etc).

Are you going to do Cloud Management?
-------------------------------------

No. Talking to cloud APIs is technically something you could do in plugins, but we suggest using a purpose-designed tool for this,
such as CloudFormation on AWS, or Terraform.

Are you going to manage Network Devices?
----------------------------------------

No. We are not experts in this field, but strongly believe tools that do this should have a graph-based representation of a discovered
network and active monitoring.  This is simply not a good fit for our architecture. OpsMop's policies will describe a local system,
and then the orchestration features to come may describe a collection of systems and the orders of application across those systems.

Are you going to support Rolling Updates?
-----------------------------------------

Maybe? We would encourage most folks to adopt Immutable Systems for cloud based deployments, and get into a red/green, blue/black, chartreuse/magenta
type deployment pattern that does not involve rolling updates over a load balancer.  However, this isn't out of question, because some of the
fine grained control to do this is useful in implementing Canary deployments, which some people are interested in.

What's The Audience For This Tool?
----------------------------------

Basically the audience for OpsMop should be the people that like OpsMop's current direction or where they like where it is going. OpsMop
should be a good fit for image preparation, management of stateful servers, deploying clouds themselves, and ad-hoc management tasks
of all kinds.

Many people want a CM tool to describe image build state, because it is hard to reuse and manage complex bash scripts for describing
image configurations.  Many people wish to apply configuration change to update their images on boot, and in this case, a pull-based
solution using git or the future opsmop pull support would be highly useful.  And of course lots of folks still need classic configuration 
and deployment tools.

We fully embrace Python3 and value exceptionally clean code and near-constant refactoring, which should keep the codebase both appealing
to new operations folks and new python developers but also very attractive to experienced Python developers.

It will not be appealing to those who do not wish to learn Python, but we strongly believe there is tremendous value in Python.

If you like Michael's past work you will probably like this tool a lot.

If you have a good idea, we can probably add it. See :ref:`community` and :ref:`development` for how to get involved with ideas,
discussion, code, and docs.

Other Questions or Bug Reports
------------------------------

See :ref:`community` for forum and GitHub information.

What's The Roadmap?
-------------------

For some short term ideas, see TODO.md in the main checkout.  This is always subject to change and we don't 
commit to any specific gameplan - good ideas always get to come first!