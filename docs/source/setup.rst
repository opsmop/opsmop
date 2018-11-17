.. _setup:

Setup
=====

* OpsMop is currently an alpha-stage application
* The first formal "release" is planned for approximately January 2019
* Following the "master" branch on GitHub is encouraged

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

If not already installed, use Homebrew:

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

And::

    source env/bin/activate

.. _checkout:

Git Checkout and Dependencies
-----------------------------

Checkout both opsmop demo and the demo content::

    git clone https://github.com/vespene-io/opsmop.git
    git clone https://github.com/vespene-io/opsmop-demo.git 

Now install python dependencies with pip:

	cd opsmop/
	make requirements

.. _first_test:	

Trying Things Out
-----------------

The other chapters will explain opsmop in greater depth, but let's see
if this works::

    bin/opsmop apply ../opsmop-demo/content/hello.py

.. _pypi:	

What About PyPi?
----------------

Versions of opsmop will be available in PyPi after the first release in 2019.

Next Steps
----------

* :ref:`local`
* :ref:`language`


