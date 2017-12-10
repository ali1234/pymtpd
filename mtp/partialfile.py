class PartialFile(object):

    def __init__(self, file, offset, length):
        self.file = file
        self.file.seek(offset, 0)
        self.offset = self.file.tell()
        self.file.seek(self.offset+length, 0)
        self.length = self.tell()
        self.file.seek(self.offset, 0)

    def read(self, n=-1):
        return self.file.read(n)

    def seek(self, offset, whence):
        if offset > self.length:
            offset = self.length

        if whence == 0:
            self.file.seek(offset+self.offset, 0)

        elif whence == 2:
            self.file.seek(self.offset+self.length-offset, 0)

        else:
            current = self.file.tell()
            new = current + offset
            if new < self.offset:
                new = self.offset
            elif new > (self.offset + self.length):
                new = self.length
            self.file.seek(new, 0)

        return self.tell()

    def tell(self):
        return self.file.tell() - self.offset
