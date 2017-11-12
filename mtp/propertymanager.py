class PropertyManager(object):
    def __init__(self, proptype, *args):
        self.__props = {}
        self.__proptype = proptype
        print(proptype)
        for arg in args:
            print(arg)
            self.__props[arg[0]] = self.__proptype(*arg)

    def keys(self):
        return self.__props.keys()

    def __getitem__(self, code):
        try:
            return self.__props[code]
        except KeyError:
            raise self.__proptype.keyerror
