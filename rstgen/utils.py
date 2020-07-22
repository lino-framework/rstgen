# -*- coding: UTF-8 -*-
# doctest rstgen/utils.py
# Copyright 2009-2020 Rumma & Ko Ltd
# License: BSD, see LICENSE for more details.

"""
Defines a series of utility classes and functions.

"""

import re
import os
import sys
import datetime
import inspect
import subprocess
from dateutil import parser as dateparser
from contextlib import contextmanager
from unipath import Path
from pprint import pprint
from importlib import import_module


def confirm(prompt=None, default="y"):
    """
    Ask for user confirmation from the console.
    """
    # if six.PY2:
    #     prompt = prompt.encode(
    #         sys.stdin.encoding or locale.getpreferredencoding(True))
    # print(20160324, type(prompt))
    prompt += " [Y,n]?"
    while True:
        ln = input(prompt)
        if not ln:
            ln = default
        if ln.lower() in ('y', 'j', 'o'):
            return True
        if ln.lower() == 'n':
            return False
        print("Please answer Y or N")

def i2d(i):
    """
    Convert `int` to `date`. Examples:

    >>> i2d(20121224)
    datetime.date(2012, 12, 24)

    """
    s = str(i)
    if len(s) != 8:
        raise Exception("Invalid date specification {0}.".format(i))
    d = dateparser.parse(s)
    d = datetime.date(d.year, d.month, d.day)
    # print(i, "->", v)
    return d


def i2t(s):
    """
    Convert `int` to `time`. Examples:

    >>> i2t(815)
    datetime.time(8, 15)

    >>> i2t(1230)
    datetime.time(12, 30)

    >>> i2t(12)
    datetime.time(12, 0)

    >>> i2t(1)
    datetime.time(1, 0)

    """
    s = str(s)
    if len(s) == 4:
        return datetime.time(int(s[:2]), int(s[2:]))
    if len(s) == 3:
        return datetime.time(int(s[:1]), int(s[1:]))
    if len(s) <= 2:
        return datetime.time(int(s), 0)
    raise ValueError(s)


def indentation(s):
    """
    Examples:

    >>> indentation("")
    0
    >>> indentation("foo")
    0
    >>> indentation(" foo")
    1

    """
    return len(s) - len(s.lstrip())


def unindent(s):
    """
    Reduces indentation of a docstring to the minimum.
    Empty lines don't count.

    Examples:

    >>> unindent('')
    ''
    >>> print(unindent('''
    ...   foo
    ...     foo
    ... '''))
    <BLANKLINE>
    foo
      foo
    >>> print(unindent('''
    ... foo
    ...     foo
    ... '''))
    <BLANKLINE>
    foo
        foo
    """
    s = s.rstrip()
    lines = s.splitlines()
    if len(lines) == 0:
        return s.strip()
    mini = sys.maxsize
    for ln in lines:
        ln = ln.rstrip()
        if len(ln) > 0:
            mini = min(mini, indentation(ln))
            if mini == 0:
                break
    if mini == sys.maxsize:
        return s
    return '\n'.join([i[mini:] for i in lines])


class SubProcessParent(object):

    """
    Base class for :class:`atelier.test.TestCase`.
    Also used standalone by `lino.management.commands.makescreenshots`.
    """
    default_environ = dict()
    # inheritable_envvars = ('VIRTUAL_ENV', 'PYTHONPATH', 'PATH')

    def build_environment(self):
        """Contructs and return a `dict` with the environment variables for
        the future subprocess.

        """
        env = dict()
        env.update(os.environ)
        env.update(self.default_environ)
        # env.update(COVERAGE_PROCESS_START="folder/.coveragerc")
        # for k in self.inheritable_envvars:
        #     v = os.environ.get(k, None)
        #     if v is not None:
        #         env[k] = v
        return env

    def check_output(self, args, **kw):
        env = self.build_environment()
        kw.update(env=env)
        kw.update(stderr=subprocess.STDOUT)
        return subprocess.check_output(args, **kw)

    def open_subprocess(self, args, **kw):
        """Additional keywords will be passed to the `Popen constructor
        <http://docs.python.org/2.7/library/subprocess.html#popen-constructor>`_.
        They can be e.g.  `cwd` : the working directory

        """
        env = self.build_environment()
        # raise Exception("20170912 {}".format(env.keys()))
        kw.update(env=env)
        #~ subprocess.check_output(args,**kw)
        #~ from StringIO import StringIO
        #~ buffer = StringIO()
        kw.update(stdout=subprocess.PIPE)
        kw.update(stderr=subprocess.STDOUT)
        kw.update(universal_newlines=True)
        return subprocess.Popen(args, **kw)

    def run_subprocess(self, args, **kw):
        """
        Run a subprocess, wait until it terminates,
        fail if the returncode is not 0.
        """
        # print ("20150214 run_subprocess %r" % args)
        p = self.open_subprocess(args, **kw)

        # wait() will deadlock when using stdout=PIPE and/or
        # stderr=PIPE and the child process generates enough output to
        # a pipe such that it blocks waiting for the OS pipe buffer to
        # accept more data. Use communicate() to avoid that.
        if False:
            p.wait()
        else:
            out, err = p.communicate()
        # raise Exception("20160711 run_subprocess", out)
        rv = p.returncode
        # kw.update(stderr=buffer)
        # rv = subprocess.call(args,**kw)
        if rv != 0:
            cmd = ' '.join(args)
            # if six.PY2:
            #     # if the output contains non-asci chars, then we must
            #     # decode here in order to wrap it into our msg. Later
            #     # we must re-encode it because exceptions, in Python
            #     # 2, don't want unicode strings.
            #     out = out.decode("utf-8")
            msg = "%s (%s) returned %d:\n-----\n%s\n-----" % (
                cmd, kw, rv, out)
            # try:
            #     msg = "%s (%s) returned %d:\n-----\n%s\n-----" % (
            #         cmd, kw, rv, out)
            # except UnicodeDecodeError:
            #     out = repr(out)
            #     msg = "%s (%s) returned %d:OOPS\n-----\n%s\n-----" % (
            #         cmd, kw, rv, out)

            # print msg
            # if six.PY2:
            #     msg = msg.encode('utf-8')
            self.fail(msg)


@contextmanager
def cd(path):
    old_dir = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(old_dir)


def srcref(mod):
    """
    Return the `source file name` for usage by Sphinx's ``srcref``
    role.  Returns None if the source file is empty (which happens
    e.g. for :file:`__init__.py` files whose only purpose is to mark a
    package).

    Examples:

    >>> import atelier
    >>> from atelier import sphinxconf
    >>> from atelier.sphinxconf import base
    >>> print(srcref(atelier))
    https://github.com/lino-framework/atelier/blob/master/atelier/__init__.py
    >>> print(srcref(sphinxconf))
    https://github.com/lino-framework/atelier/blob/master/atelier/sphinxconf/__init__.py
    >>> print(srcref(base))
    https://github.com/lino-framework/atelier/blob/master/atelier/sphinxconf/base.py
    """
    root_module_name = mod.__name__.split('.')[0]
    root_mod = __import__(root_module_name)
    srcref_url = getattr(root_mod, 'srcref_url', None)
    if srcref_url is None:
        # print(20180126, root_module_name, root_mod, srcref_url)
        return
    #~ if not mod.__name__.startswith('lino.'):
        #~ return
    srcref = mod.__file__
    if srcref.endswith('.pyc'):
        srcref = srcref[:-1]
    if True:
        # failed on readthedocs.org because there was a dangling pyc
        # file on my machine which caused autodoc to create an entry
        # in docs/api.
        if os.stat(srcref).st_size == 0:
            return
    #~ srcref = srcref[len(lino.__file__)-17:]
    root = Path(root_mod.__file__).ancestor(2)
    if len(root):
        srcref = srcref[len(root) + 1:]
    srcref = srcref.replace(os.path.sep, '/')
    return srcref_url % srcref


def import_from_dotted_path(dotted_names, path=None):
    """
    Thanks to Chase Seibert,
    https://chase-seibert.github.io/blog/2014/04/23/python-imp-examples.html
    """

    s = dotted_names.split('.', 1)
    if len(s) == 2:
        first, remaining = s
    else:
        first, remaining = dotted_names, None
    fp, pathname, description = importlib.find_module(first, path)
    module = importlib.load_module(first, fp, pathname, description)
    if not remaining:
        return (module, None)
    if hasattr(module, remaining):
        return (module, getattr(module, remaining))
    return import_from_dotted_path(remaining, path=module.__path__)


def py2url_txt(s):
    """
    Return a tuple `(url, txt)` where `url` is the URL which links to
    the source code of the specified Python object and `txt` is the
    suggested short text to use in a hyperlink.
    """
    args = s.split(None, 1)
    if len(args) == 1:
        txt = s
    else:
        s = args[0]
        txt = args[1]

    if False:
        try:
            mod, obj = import_from_dotted_path(s)
            return (srcref(mod), txt)
        except Exception as e:
            return ("Error in Python code ({})".format(e), txt)
    parts = s.split('.')
    try:
        obj = import_module(parts[0])
        for p in parts[1:]:
            obj = getattr(obj, p)
        mod = inspect.getmodule(obj)
        return (srcref(mod), txt)
    except Exception as e:
        return ("Error in Python code ({})".format(e), txt)
