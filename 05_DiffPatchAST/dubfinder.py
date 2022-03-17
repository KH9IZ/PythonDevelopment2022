import difflib
import itertools
import ast
import textwrap
import sys
import inspect
import importlib

def func_finder(obj):
    res = {}
    for name, value in inspect.getmembers(obj):
        if inspect.isclass(value) and not name.startswith('__'):
            res |= func_finder(value)
        elif inspect.isfunction(value):
            fname = list(value.__qualname__.rpartition('.'))
            fname[-1] = name
            fname = ''.join(fname)
            res[fname] = value
    return res


o = {}
for arg in sys.argv[1:]:
    module = importlib.import_module(arg)
    prefix = module.__name__
    for fname, func in func_finder(module).items():
        name = f"{prefix}.{fname}"
        src = inspect.getsource(func)
        src = textwrap.dedent(src)
        tree = ast.parse(src)
        for item in ast.walk(tree):
            if getattr(item, 'id', None) is not None:
                item.id = '_'
            if getattr(item, 'name', None) is not None:
                item.name = '_'
            if getattr(item, 'arg', None) is not None:
                item.arg = '_'
            if getattr(item, 'attr', None) is not None:
                item.attr = '_'
        o[name] = ast.unparse(tree)

o = dict(sorted(o.items(), key=lambda x: x[0].rpartition('.')[-1]))
print(o.keys())
for one, another in itertools.combinations(o.items(), 2):
    if difflib.SequenceMatcher(None, one[1], another[1]).ratio() > 0.95:
        print(one[0], another[0])
