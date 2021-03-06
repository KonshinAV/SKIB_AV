import base64

def encoding (string):
    b1 = string.encode("UTF-8")
    e1 = base64.b64encode(b1).decode("UTF-8")[::-1]
    b2 = e1.encode("UTF-8")
    e2 = base64.b64encode(b2).decode("UTF-8")
    return (f'{e2}')

def decoding (string):
    try:
        b1 = string.encode("UTF-8")
        d1 = base64.b64decode(b1)[::-1]
        d2 = base64.b64decode(d1).decode("UTF-8")
        return (f'{d2}')
    except Exception as ex:
        return (False,ex)
