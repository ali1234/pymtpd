from construct import Adapter, PrefixedArray, Byte, Int16ul


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


if __name__ == '__main__':

    print(MTPString.build(''))
    print(MTPString.build('A'))
    print(MTPString.build('hello'))

    print(MTPString.parse(b'\x00'))
    print(MTPString.parse(b'\x02A\x00\x00\x00'))
    print(MTPString.parse(b'\x06h\x00e\x00l\x00l\x00o\x00\x00\x00'))

