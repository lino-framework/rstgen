# -*- coding: utf-8 -*-
# Copyright 2016-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""A Sphinx extension that adds the :rst:dir:`refstothis` directive.

Thanks to Tomasz Czyż who inspired me to write this.  His
`sphinxcontrib-taglist
<https://github.com/spinus/sphinxcontrib-taglist>`_ module uses a
different approach, based on the idea that every "reference" to a tag
also specifies a text to appear in the list of references.
:rst:dir:`refstothis` is for people who don't want to specify their
own text for each tag directive.

TODO:

- When I do :cmd:`inv clean` followed by :cmd:`inv bd`, then e.g. the
  `refstothis` in :doc:`/refstothis/baz` does not mention all other documents.
  But when I then touch the `baz.rst` file and run :cmd:`inv bd`, then they are
  all there.  I guess this is because not all documents have been loaded when
  the rst is being generated.

"""


from os import path
import time
from pprint import pprint
from sphinx import addnodes
from sphinx.util import docname_join
import rstgen

from .insert_input import InsertInputDirective


def py2rst(x):
    x = pprint(x)
    # x  = x.replace("|","")
    return x


class RefsToThis(InsertInputDirective):
    """Implements the rst:dir:`refstothis` directive."""

    # debug = True

    def get_rst(self):
        # return str(self.state.document.refnames)
        env = self.state.document.settings.env
        # print("20211108", self.content)
        targets = set(self.content)
        if len(targets) == 0:
            targets = {env.temp_data['docname']}
        # target = ' '.join(self.content).strip()
        # if not target:
        #     # print("20140409 target is %r" % target)
        found = set()
        rows = set()

        # headers = 'children attributes \
        # resolved referenced indirect_reference_name \
        # tagname'.split()

        for docname in env.found_docs:
            if env.temp_data['docname'] == docname:  # skip myself
                continue

            try:
                doc = env.get_doctree(docname)
            except Exception:
                # 20140117 i had the following after a fab clean:
                #   File "/home/luc/pythonenvs/py27/local/lib/python2.7/site-packages/sphinx/environment.py", line 1077, in get_doctree
                #     f = open(doctree_filename, 'rb')
                # IOError: [Errno 2] No such file or directory: u'/home/luc/hgwork/lino/docs/.build/.doctrees/topics/names.doctree'

                continue

            # print("20140115 traversing", docname)
            for ref in doc.traverse(addnodes.pending_xref):
                if ref['reftype'] == 'doc':
                    other = docname_join(ref['refdoc'], ref['reftarget'])
                else:
                    other = ref['reftarget']
                if other in targets:
                    found.add(ref['refdoc'])
                    # print("20140409 found", ref)
                else:
                    # rows.add(ref['reftarget'])
                    rows.add(other)
                    # rows.add(repr(ref.attributes))
                    # row = []
                    # for h in headers:
                    #     row.append(py2rst(getattr(ref, h, 'N/A')))
                    # rows.append(unicode(row))

        if len(found) == 0:
            s = """No documents found for targets %r.""" % targets
            # s += """\nPending xrefs were %r.""" % rows
            return s

        entries = []
        for refdoc in found:
            mtime = path.getmtime(env.doc2path(refdoc))
            entries.append((mtime, refdoc))

        def f(a):
            return a[0]
        entries.sort(key=f)
        entries.reverse()

        # from time import strftime

        items = [':doc:`/%(doc)s` (%(time)s)' % dict(
            time=time.ctime(e[0]),
            doc=e[1]) for e in entries]

        if 'debug' in self.options:
            items.append("DEBUG: pending xrefs were %r." % rows)

        return rstgen.ul(items)


def setup(app):
    app.add_directive('refstothis', RefsToThis)
