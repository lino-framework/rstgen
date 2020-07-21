=================
The rstgen module
=================

rstgen is a library of utilities to programmatically generate chunks of
`reStructuredText <http://docutils.sourceforge.net/rst.html>`__.  It is being
used e.g. by `atelier`, `etgen` and `lino`.

Kevin Horn wrote and maintains a comparable library, also called
`rstgen <https://bitbucket.org/khorn/rstgen/src>`_. (TODO: Check
whether we should join our efforts.)


.. function:: header(level, text)

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



.. function:: table(headers, rows=tuple(), **kw)

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

The simplest case of :func:`table`:

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

You might prefer to use directly the :class:`Table` class:

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
