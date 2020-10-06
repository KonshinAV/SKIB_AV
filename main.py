from utils import secure_string
from utils.nettools import test_tcp_port_connection

if __name__ == '__main__':
    pwd = secure_string.SecureString("Pass")
    print (pwd.encoding())
    print (test_tcp_port_connection('192.168.31.1',445))
    pass
