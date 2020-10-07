from utils import secure_string
from utils.nettools import test_tcp_port_connection
import os
from utils.adtools import test_ad_con

if __name__ == '__main__':
    pwd = secure_string.SecureString("P@$$w0rd")
    print (pwd.encoding())
    # print (test_tcp_port_connection('192.168.31.1',445))
    for i in range(100):
        print(f"query: {i}\n"
              f"{os.getlogin()}\n"
              f"{os.getcwd()}\n"
              f"Test gateway: {test_tcp_port_connection('192.168.31.1',445)}\n"
              f"Ad_conn {test_ad_con()}")
    pass
