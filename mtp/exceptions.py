class MTPError(Exception):
    def __init__(self, code, params=()):
        super().__init__(code)
        self.code = code
        self.params = params
