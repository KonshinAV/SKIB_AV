import socket

def test_tcp_port_connection (target, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect((target,port))
        s.close()
        return True
    except Exception as ex:
        return (False, ex)
    pass