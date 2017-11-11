from construct import *
from construct.lib import *

class Term(Adapter):
    def _encode(self, obj, ctx):
        return obj + ([0] if len(obj) > 0 else [])
    def _decode(self, obj, ctx):
        return obj[:-1]


class SL(Adapter):
    def _encode(self, obj, ctx):
        return [ord(c) for c in obj]
    def _decode(self, obj, ctx):
        return u''.join(chr(i) for i in obj)


MTPString = SL(Term(PrefixedArray(Byte, Int16ul)))
