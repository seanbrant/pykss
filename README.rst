PyKSS - Knyle Style Sheets
==========================

.. image:: https://secure.travis-ci.org/seanbrant/pykss.png?branch=master
   :target: http://travis-ci.org/seanbrant/pykss


PyKSS is a Python implementation of KSS_. KSS attempts to provide a
methodology for writing maintainable, documented CSS within a team.

The official docs_ provide a good introduction to KSS. The complete
syntax can he found on the syntax_ page.

.. _KSS: http://warpspire.com/kss
.. _docs: http://warpspire.com/kss/
.. _syntax: http://warpspire.com/kss/syntax/


Installing
----------

.. code-block:: shell

    pip install pykss


Usage
-----

.. code-block:: python

    >>> import pykss
    >>>
    >>> styleguide = pykss.Parser('static/css')
    >>>
    >>> styleguide.section('2.1.1')
    <pykss.section.Section object at 0x10c1d1190>
    >>>
    >>> styleguide.section('2.1.1').description
    'A button suitable for giving stars to someone.'
    >>>
    >>> styleguide.section('2.1.1').modifiers[0]
    <pykss.modifier.Modifier object at 0x10c1d1290>
    >>>
    >>> styleguide.section('2.1.1').modifiers[0].name
    ':hover'
    >>>
    >>> styleguide.section('2.1.1').modifiers[0].class_name
    'pseudo-class-hover'
    >>>
    >>> styleguide.section('2.1.1').modifiers[0].description
    'Subtle hover highlight'


Django Usage
------------
If you would like to use KSS within a Django project `pykss.contrib.django`
provides a view and template tag to make it easier. Check out the example
Django project for usage.
