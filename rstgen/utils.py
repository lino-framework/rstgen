# -*- coding: UTF-8 -*-
# doctest rstgen/utils.py
# Copyright 2009-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

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
from pathlib import Path
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
            cmd = ' '.join(map(str, args))  # args can contain PosixPath instances
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


def srcref_url_template(mod):
    root_mod_name = mod.__name__.split('.')[0]
    root_mod = __import__(root_mod_name)
    setup_info = getattr(root_mod, 'SETUP_INFO', {})
    url = setup_info.get('url')
    if url is None:
        return (root_mod, None)
    if not url.endswith('/'):
        url += "/"
    # srcref_url = getattr(root_mod, 'srcref_url', None)
    # if srcref_url is None:
    #     # print(20180126, root_module_name, root_mod, srcref_url)
    #     return
    #~ if not mod.__name__.startswith('lino.'):
        #~ return
    return (root_mod, url + "blob/master/%s")

def srcref(mod):
    root_mod, tpl = srcref_url_template(mod)
    if tpl is None:
        return
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
    root = str(Path(root_mod.__file__).parents[1])
    if len(root):
        srcref = srcref[len(root) + 1:]
    srcref = srcref.replace(os.path.sep, '/')
    return tpl % srcref


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


def dict_py2(old_dict):
    """Convert the given `dict` so that it's `repr` is the same for both
    Python 2 and 3.

    Deprecated. Use :func:`rmu` instead.
    """
    from future.utils import viewitems
    new_dict = {}
    for (key, value) in viewitems(old_dict):
        if type(value) == dict:
            new_dict[str(key)] = dict_py2(value)
        elif type(value) == list:
            new_dict[str(key)] = list_py2(value)
        elif type(value) == tuple:
            new_dict[str(key)] = tuple_py2(value)
        else:
            if isinstance(value, bool):
                new_dict[str(key)] = value
            else:
                new_dict[str(key)] = str(value)
    return new_dict


def list_py2(old_list):
    """Convert the given `list` so that it's `repr` is the same for both
    Python 2 and 3.

    Deprecated. Use :func:`rmu` instead.

    """
    new_list = []
    for item in old_list:
        if type(item) == dict:
            new_list.append(dict_py2(item))
        elif type(item) == tuple:
            new_list.append(tuple_py2(item))
        else:
            new_list.append(str(item))
    return new_list


def tuple_py2(old_tuple):
    """Convert the given `tuple` so that it's `repr` is the same for both
    Python 2 and 3.

    Deprecated. Use :func:`rmu` instead.

    """
    lst = list(old_tuple)
    lst = list_py2(lst)
    return tuple(lst)


def rmu(x):
    """Remove the 'u' prefix from unicode strings under Python 2 in order
    to produce Python 3 compatible output in a doctested code snippet.

    >>> lst = [123, "123", u"Äöü"]
    >>> print(rmu(lst))
    [123, '123', '\\xc4\\xf6\\xfc']
    >>> print(rmu(tuple(lst)))
    (123, '123', '\\xc4\\xf6\\xfc')
    >>> dct = {i: i for i in lst}
    >>> print(rmu(dct)) #doctest: +ELLIPSIS
    {...'\\xc4\\xf6\\xfc': '\\xc4\\xf6\\xfc'...}

    """
    if isinstance(x, Path):
        return x
    # if isinstance(x, collections.namedtuple):
    #     return x
    if isinstance(x, list):
        return [rmu(i) for i in x]
    if isinstance(x, tuple):
        return tuple([rmu(i) for i in x])
    if isinstance(x, dict):
        return {rmu(k):rmu(v) for k,v in x.items()}
    if isinstance(x, str):
        return str(x)
    return x


def sixprint(*args):
    """Like print, but simulating PY3 output under PY2."""
    for x in args:
        # if six.PY2 and isinstance(x, set):
        #     print("{%s}" % ', '.join([str(rmu(i)) for i in x]))
        # else:
        pprint(rmu(x))
