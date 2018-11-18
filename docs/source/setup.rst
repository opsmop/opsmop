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

And::

    source env/bin/activate

.. _checkout:

Git Checkout and Dependencies
-----------------------------

Checkout both opsmop demo and the demo content::

    git clone https://github.com/opsmop/opsmop.git
    git clone https://github.com/opsmop/opsmop-demo.git 

Don't forget about that demo repo!  It's the best way to learn OpsMop.

Now install python dependencies with pip::

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


