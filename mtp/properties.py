class Properties(object):
    def __init__(self, proptype, *args):
        self._props = {}
        self._proptype = proptype
        for arg in args:
            self._props[arg[0]] = self._proptype(*arg)

    def keys(self):
        return self._props.keys()

    def values(self):
        return self._props.values()

    def items(self):
        return self._props.items()

    def __getitem__(self, code):
        try:
            return self._props[code]
        except KeyError:
            if hasattr(self._proptype, 'keyerror'):
                raise self._proptype.keyerror
            else:
                raise
