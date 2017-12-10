import io

from mtp.exceptions import MTPError
from mtp.packets import indata, outdata

class Registry(object):
    def __init__(self):
        self.operations = {}

    def __getitem__(self, name):
        try:
            return self.operations[name]
        except KeyError:
            raise MTPError('OPERATION_NOT_SUPPORTED')

    def keys(self):
        return self.operations.keys()

    def register(self, fn, name):
        self.operations[name] = fn

    def __call__(self, fn):
        """Basic decorator for operations."""
        self.register(fn, fn.__name__)
        return fn

    def session(self, fn):
        """Decorator for operations which require a session to be open.

        Returns a SESSION_NOT_OPEN response if no session is open,
        otherwise it calls the handler.
        """

        def check_session(self, *args):
            if self.session_id is None:
                raise MTPError('SESSION_NOT_OPEN')
            else:
                return fn(self, *args)

        self.register(check_session, fn.__name__)
        return check_session

    def filereceiver(self, fn):
        """Decorator for operations which receive data from the inquirer.

        The data stage must run even if there is an error with the operation.
        """
        def receivefile(self, p):
            if self.session_id is None:
                raise MTPError('SESSION_NOT_OPEN')
            else:
                try:
                    (dest, params) = fn(self, p)
                except MTPError as e:
                    outdata(self.outep, p.code, p.tx_id, open('/dev/null', 'wb'))
                    raise e
                else:
                    outdata(self.outep, p.code, p.tx_id, dest)
                    return params

        self.register(receivefile, fn.__name__)
        return receivefile

    def receiver(self, fn):
        """Decorator for operations which receive data from the inquirer.

        The data stage must run even if there is an error with the operation.
        """

        def receivedata(self, p):
            if self.session_id is None:
                raise MTPError('SESSION_NOT_OPEN')
            else:
                bio = io.BytesIO()
                outdata(self.outep, p.code, p.tx_id, bio)
                return fn(self, p, bytes(bio.getbuffer()))

        self.register(receivedata, fn.__name__)
        return receivedata

    def sender(self, fn):
        """Decorator for operations which send data to the inquirer.

        The data stage must run even if there is an error with the operation.
        """

        def senddata(self, p):
            if self.session_id is None:
                raise MTPError('SESSION_NOT_OPEN')
            else:
                try:
                    (data, params) = fn(self, p)
                except MTPError as e:
                    indata(self.inep, p.code, p.tx_id, io.BytesIO(b''))
                    raise e
                else:
                    indata(self.inep, p.code, p.tx_id, data)
                    return params

        self.register(senddata, fn.__name__)
        return senddata

