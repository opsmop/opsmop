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

This is a long question, best answered by reading through the documentation and trying things for yourself.

If X is a configuration management system, the quickest answer is that OpsMop is completely open ended, and supports
arbitrary code.  There is no "DSL" anywhere, just an RPC system with an integrated library.

It is designed around runtime performance, developer efficiency (both in modules and language) and ultimate flexibility.

We believe you shouldn't need to keep a lot of things floating around in your head when using an automation tool, so OpsMop
exposes Python wherever it can.

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

The "name" parameter should take an array in the near future, but what's wrong with the shell command?  Nothing, really.

Push vs Pull vs Local - What Does OpsMop Do?
--------------------------------------------

Right now, OpsMop is :ref:`local` and :ref:`push` (SSH) only - but highly-pluggable pull modes will likely be added in the future.

I Have A Develoment Question?
-----------------------------

Great! Thanks for the interest! Please check out :ref:`development`!  We would be glad to help you with pull requests, and also feel
free to stop by the forum listed on :ref:`community` with development questions.


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

You could technically write a bridge module, but it's not something we want for the core program, as we think
there is a very strong reason for everybody collaborating around using the same language.

OpsMop modules take advantage of a lot of features for code reuse.  We also minimize forking to
maintain execution speed.

This is to not say you couldn't invoke a shell script, or a program in some other language, and record the output
and return code, which you can still of course do, either. 

How Do I Do (Complicated Thing Without A Module)
------------------------------------------------

There really needs to be a Script module feature to make this easier very soon, but if you don't feel like writing a type & provider, OpsMop can always
push a script::

    File(name="/opt/opsmop/", directory=True),
    File(name="/opt/opsmop/setup.sh", from_file="files/setup.sh"),
    Shell("bash /opt/opsmop/setup.sh")

Just return 0 on success and non-zero on failure.
  
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

Do you support Rolling Updates?
-------------------------------

Yes, see :ref:`push_advanced_tricks`.

We would encourage most folks to adopt Immutable Systems for cloud based deployments, and get into a red/green, blue/black, chartreuse/magenta
type deployment pattern that does not involve rolling updates over a load balancer where you can, but the push mode orchestrator is exceptionally
flexible and is designed for this sort of thing.

Other Questions or Bug Reports
------------------------------

See :ref:`community` for forum and GitHub information.
