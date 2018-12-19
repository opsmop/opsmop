.. image:: opsmop.png
   :alt: OpsMop Logo

.. _setup:

Setup
=====

* OpsMop is still new so these instructions describe running from a git checkout only.
* Versioned releases to PyPi will occur in 2019.

.. _python3:

Python 3
--------

OpsMop requires Python 3.  

.. _python3_linux:

Python 3 on Linux/Unix
----------------------

Skills test!

If needed, please install Python 3.6 or higher.

.. _python3mac:

Python 3 on Mac OS X
--------------------

If not already installed, use Homebrew::

    brew install Python

And::
    
    # vim ~/.bashrc
    export path=/usr/local/bin:$PATH
    alias python /usr/local/bin/python3

And::

    source ~/.bashrc

And::

    easy_install-3.7 virtualenv
    virtualenv env -p /usr/local/bin/python3
    source env/bin/activate

.. _pip_install:

Pip Install
-----------

On your platform, python 3 pip may be named 'pip3' or something like 'pip-3.6' or 'pip-3.7'.  
Please make sure you use Python 3's pip as OpsMop is a Python 3 application/library.

To install OpsMop directly from pip::

     pip install git+https://github.com/opsmop/opsmop.git@master

Opsmop will have official versions on PyPi in early 2019, but we still strongly suggest tracking
the git repository. It is always intendeded to be usable, and will allow trying out new features
immediately as they become available.

To update to the latest code at any time, simply repeat the above command.

.. _checkout:

Alternative: Installing From Source
-----------------------------------

Checkout both opsmop repo::

    git clone https://github.com/opsmop/opsmop.git

Now install python dependencies with pip::

	cd opsmop/
	make requirements

.. _demo_repo:

Checkout The Demo Repo
----------------------

The 'opsmop-demo' repo contains OpsMop learning examples.  Many are abstract and do not install
real things, but they are there to teach you about the language and the tools::

    git clone https://github.com/opsmop/opsmop-demo.git 

.. _first_test:	

Trying Things Out
-----------------

The other chapters will explain opsmop in greater depth, but let's see
if this works, just running from source::

    cd opsmop-demo/content
    PYTHONPATH=/path/for/checkout/of/opsmop python3 hello.py --local --apply
    
.. _pypi:	

What About PyPi?
----------------

Versions of opsmop will be available in PyPi after the first release in 2019.

The instructions above discuss running from source, which is useful if you are developing
on the program.  Once installed, everything will work the same way, except PYTHONPATH
will not need to be set.

You can of course also "chmod +x" any policy file to avoid having to specify the interpreter.

Setup Problems or Questions?
----------------------------

There are lots of new things and some part of the documentation may even be lies!
Actually no, but we're working on a lot of things yet. We'd love to help you out and
hear about what you want to do. Stop by the :ref:`forum` and get to know us.
Understanding what you want to do helps us build a better OpsMop.

Next Steps
----------

* :ref:`local`
* :ref:`language`


