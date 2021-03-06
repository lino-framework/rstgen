=====================
The ``rstgen`` module
=====================

rstgen is a library of utilities to programmatically generate chunks of
`reStructuredText <http://docutils.sourceforge.net/rst.html>`__.  It is being
used e.g. by `atelier`, `etgen` and `lino`.

Kevin Horn wrote and maintains a comparable library, also called
`rstgen <https://bitbucket.org/khorn/rstgen/src>`_. (TODO: Check
whether we should join our efforts.)

Source code: https://github.com/lino-framework/rstgen

The ``header(level, text)`` function
====================================

Render the text as a header with the specified level.

It uses and supposes the following system of header levels::

   =======
   Level 1
   =======

   -------
   Level 2
   -------

   ~~~~~~~
   Level 3
   ~~~~~~~

   Level 4
   =======

   Level 5
   -------

   Level 6
   ~~~~~~~



The ``table(headers, rows=tuple(), **kw)`` function
===================================================

Convert the given headers and rows into an reStructuredText formatted table.

- `headers` is an iterable of strings, one for each column
- `rows` is an iterable of rows, each row being an iterable of strings.

.. rubric:: Usage examples

Here is the data we are going to render into different tables:

>>> headers = ["Country", "City", "Name"]
>>> rows = []
>>> rows.append(["Belgium", "Eupen", "Gerd"])
>>> rows.append(["Estonia", "Vigala", "Luc"])
>>> rows.append(["St. Vincent and the Grenadines", "Chateaubelair", "Nicole"])

The simplest case of ``table()``:

>>> from rstgen import table
>>> print(table(headers, rows))
================================ =============== ========
 Country                          City            Name
-------------------------------- --------------- --------
 Belgium                          Eupen           Gerd
 Estonia                          Vigala          Luc
 St. Vincent and the Grenadines   Chateaubelair   Nicole
================================ =============== ========
<BLANKLINE>

Result:

================================ =============== ========
 Country                          City            Name
-------------------------------- --------------- --------
 Belgium                          Eupen           Gerd
 Estonia                          Vigala          Luc
 St. Vincent and the Grenadines   Chateaubelair   Nicole
================================ =============== ========

A table without headers:

>>> print(table(headers, rows, show_headers=False))
================================ =============== ========
 Belgium                          Eupen           Gerd
 Estonia                          Vigala          Luc
 St. Vincent and the Grenadines   Chateaubelair   Nicole
================================ =============== ========
<BLANKLINE>


Result:

================================ =============== ========
 Belgium                          Eupen           Gerd
 Estonia                          Vigala          Luc
 St. Vincent and the Grenadines   Chateaubelair   Nicole
================================ =============== ========

You might prefer to use directly the ``Table`` class:

>>> from rstgen import Table
>>> t = Table(headers)
>>> print(t.to_rst(rows))
================================ =============== ========
 Country                          City            Name
-------------------------------- --------------- --------
 Belgium                          Eupen           Gerd
 Estonia                          Vigala          Luc
 St. Vincent and the Grenadines   Chateaubelair   Nicole
================================ =============== ========
<BLANKLINE>

Result:

================================ =============== ========
 Country                          City            Name
-------------------------------- --------------- --------
 Belgium                          Eupen           Gerd
 Estonia                          Vigala          Luc
 St. Vincent and the Grenadines   Chateaubelair   Nicole
================================ =============== ========

If there is at least one cell that contains a newline character,
the result will be a complex table:

>>> rows[2] = ['''St. Vincent
... and the Grenadines''',"Chateaubelair","Nicole"]
>>> print(table(headers,rows))
+--------------------+---------------+--------+
| Country            | City          | Name   |
+====================+===============+========+
| Belgium            | Eupen         | Gerd   |
+--------------------+---------------+--------+
| Estonia            | Vigala        | Luc    |
+--------------------+---------------+--------+
| St. Vincent        | Chateaubelair | Nicole |
| and the Grenadines |               |        |
+--------------------+---------------+--------+
<BLANKLINE>

Result:

+--------------------+---------------+--------+
| Country            | City          | Name   |
+====================+===============+========+
| Belgium            | Eupen         | Gerd   |
+--------------------+---------------+--------+
| Estonia            | Vigala        | Luc    |
+--------------------+---------------+--------+
| St. Vincent        | Chateaubelair | Nicole |
| and the Grenadines |               |        |
+--------------------+---------------+--------+


.. rubric:: Empty tables

A special case is a table with no rows.  For ``table(headers, [])``
the following output would be logical::

    ========= ====== ======
     Country   City   Name
    --------- ------ ------
    ========= ====== ======

But Sphinx would consider this a malformed table.  That's why we
return a blank line when there are no rows:

>>> print(table(headers, []))
<BLANKLINE>
<BLANKLINE>


The ``srcref()`` function
===========================

Return the source file name of a module, for usage by Sphinx's ``srcref`` role.
Returns `None` if the source file is empty (which happens e.g. for
``__init__.py`` files whose only purpose is to mark a package).

Examples:

>>> from rstgen.utils import srcref
>>> import atelier
>>> from atelier import sphinxconf
>>> from atelier.sphinxconf import base
>>> print(srcref(atelier))
https://github.com/lino-framework/atelier/blob/master/atelier/__init__.py
>>> print(srcref(sphinxconf))
https://github.com/lino-framework/atelier/blob/master/atelier/sphinxconf/__init__.py
>>> print(srcref(base))
https://github.com/lino-framework/atelier/blob/master/atelier/sphinxconf/base.py

The module must have an attribute ``srcref_url``. If it doesn't, ``srcref()``
returns `None`.

>>> import pathlib
>>> print(srcref(pathlib))
None



Changelog
=========

2021-03-06 Use pathlib instead of unipath
