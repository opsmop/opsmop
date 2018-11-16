Module Index
------------

Parameters and examples are given for all of the modules that ship with OpsMop.
To learn how to write your own see :ref:`plugin_development`.

Generic Modules
===============

Some of the most commonly used modules

* :ref:`module_file` - handles copy, templates, ownership, etc
* :ref:`module_shell` - executes shell commands

Platform Specific
=================

These modules have multiple provider implementations to choose from.

* :ref:`module_package` - installation, upgrades, and removal
* :ref:`module_service` - starting, stopping, and enablement status

Utilities
=========

* :ref:`module_assert` - fails policy applicaiton when conditions are false
* :ref:`module_debug` - outputs variable values
* :ref:`module_echo` - prints templated messages to the console, supports cowsay
* :ref:`module_set` - stores values in variables
* :ref:`module_stop` - halts the policy application with an error

Coming Soon
===========

Some potential favorites.

* Say - speech synthesis
* SetGlobal - stores a value in global scope
* Wait - timed delays, user input prompts, and more


