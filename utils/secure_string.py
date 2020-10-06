import base64


class SecureString:
    def __init__(self, string):
        self.string = string

    def encoding (self):
        b1 = self.string.encode("UTF-8")
        e1 = base64.b64encode(b1).decode("UTF-8")[::-1]
        b2 = e1.encode("UTF-8")
        e2 = base64.b64encode(b2).decode("UTF-8")
        return (f'{e2}')

    def decoding (self):
        try:
            b1 = self.string.encode("UTF-8")
            d1 = base64.b64decode(b1)[::-1]
            d2 = base64.b64decode(d1).decode("UTF-8")
            return (f'{d2}')
        except Exception as ex:
            return (False,ex)
