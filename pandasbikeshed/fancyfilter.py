import pandas as pd
import numpy as np
from functools import partial

def _try_call(obj, arg):
    if callable(obj):
        return obj(arg, internal=True)
    else:
        return obj
#
class BasicFilter(object):
    def __init__(self):
        pass

    def __call__(self, pd_obj, internal=False):
        if internal:
            return pd_obj
        else:
            return slice(None)

    # illegal operations
    def __delattr__(self, name):
        raise AttributeError('Filter objects are read-only! You can not delete attributes!')

    def __setitem__(self, name, value):
        raise AttributeError('Filter objects are read-only! You can not assign to them via = or :=')

    def __delitem__(self, name):
        raise AttributeError('Filter objects are read-only! You can not delete attributes!')

    # Allow indexing
    def __getattr__(self, name):
        if self.__class__ is not BasicFilter:
            raise AttributeError('Can not index into an already processing filter objedt')
        return IndexedFilter(name)

    def __getitem__(self, name):
        if self.__class__ is not BasicFilter:
            raise AttributeError('Can not index into an already processing filter objedt')
        return IndexedFilter(name)

    ## Overloading of the necessary operators

    # Comparison
    def __eq__(self, value):
        return OpsFilter(self, lambda x, inner: inner(x) == _try_call(value, x))

    def __ne__(self, value):
        return OpsFilter(self, lambda x, inner: inner(x) != _try_call(value, x))

    def __gt__(self, value):
        return OpsFilter(self, lambda x, inner: inner(x) > _try_call(value, x))

    def __ge__(self, value):
        return OpsFilter(self, lambda x, inner: inner(x) >= _try_call(value, x))

    def __lt__(self, value):
        return OpsFilter(self, lambda x, inner: inner(x) < _try_call(value, x))

    def __le__(self, value):
        return OpsFilter(self, lambda x, inner: inner(x) <= _try_call(value, x))

    # Math
    def __add__(self, value):
        return OpsFilter(self, lambda x, inner: inner(x) + _try_call(value, x))

    def __sub__(self, value):
        return OpsFilter(self, lambda x, inner: inner(x) - _try_call(value, x))

    def __mul__(self, value):
        return OpsFilter(self, lambda x, inner: inner(x) * _try_call(value, x))

    def __truediv__(self, value):
        return OpsFilter(self, lambda x, inner: inner(x) / _try_call(value, x))

    def __floordiv__(self, value):
        return OpsFilter(self, lambda x, inner: inner(x) // _try_call(value, x))

    def __pow__(self, value):
        return OpsFilter(self, lambda x, inner: inner(x) ** _try_call(value, x))

    def __mod__(self, value):
        return OpsFilter(self, lambda x, inner: inner(x) % _try_call(value, x))

    # Reverse Math

    def __radd__(self, value):
        return OpsFilter(self, lambda x, inner: _try_call(value, x) + inner(x))

    def __rsub__(self, value):
        return OpsFilter(self, lambda x, inner: _try_call(value, x) - inner(x))

    def __rmul__(self, value):
        return OpsFilter(self, lambda x, inner: _try_call(value, x) * inner(x))

    def __rtruediv__(self, value):
        return OpsFilter(self, lambda x, inner: _try_call(value, x) / inner(x))

    def __rfloordiv__(self, value):
        return OpsFilter(self, lambda x, inner: _try_call(value, x) // inner(x))

    def __rpow__(self, value):
        return OpsFilter(self, lambda x, inner: _try_call(value, x) ** inner(x))

    def __rmod__(self, value):
        return OpsFilter(self, lambda x, inner: _try_call(value, x) % inner(x))

    # Mathematical negation
    def __neg__(self):
        return OpsFilter(self, lambda x, inner: -inner(x))

    # Add custom operations here
    def isin(self, value):
        return OpsFilter(self, lambda x, inner: inner(x).isin(_try_call(value, x)))

    def notin(self, value):
        return OpsFilter(self, lambda x, inner: ~inner(x).isin(_try_call(value, x)))

    def isna(self):
        return OpsFilter(self, lambda x, inner: inner(x).isna())

    def notna(self):
        return OpsFilter(self, lambda x, inner: inner(x).notna())

    def isfinite(self):
        return OpsFilter(self, lambda x, inner: np.isfinite(inner(x)))

    # Logical connections
    def __invert__(self):
        return OpsFilter(self, lambda x, inner: ~inner(x))

    def __and__(self, other):
        return OpsFilter(self, lambda x, inner: inner(x) & _try_call(other, x))

    def __or__(self, other):
        return OpsFilter(self, lambda x, inner: inner(x) | _try_call(other, x))

    def __xor__(self, other):
        return OpsFilter(self, lambda x, inner: inner(x) ^ _try_call(other, x))

    # reversed operations (won't accept numpy etc.)
    def __rand__(self, value):
        return OpsFilter(self, lambda x, inner: _try_call(value, x) & inner(x))

    def __ror__(self, value):
        return OpsFilter(self, lambda x, inner: _try_call(value, x) | inner(x))

    def __rxor__(self, value):
        return OpsFilter(self, lambda x, inner: _try_call(value, x) ^ inner(x))


class IndexedFilter(BasicFilter):
    def __init__(self, index_name):
        if not isinstance(index_name, str):
            raise TypeError('The filter indexer can only be used with column names as str')
        self._col = index_name
    def __call__(self, pd_obj, internal=False):
        try:
            result = pd_obj[self._col]
        except KeyError:
            try:
                result = pd_obj.index.get_level_values(self._col)
            except:
                raise KeyError(f'Name {self._col} not found in columns or index')
        if internal:
            return result
        else:
            return result.astype('bool')

class OpsFilter(BasicFilter):
    def __init__(self, filter_obj, operation):
        self._op = operation
        self._inner_filter = None
        if filter_obj.__class__ is not BasicFilter:
            self._inner_filter = filter_obj

    def __call__(self, pd_obj, internal=False):
        if self._inner_filter is None:
            return self._op(pd_obj, lambda x: x)
        else:
            return self._op(pd_obj, partial(self._inner_filter, internal=True))


me=BasicFilter()
