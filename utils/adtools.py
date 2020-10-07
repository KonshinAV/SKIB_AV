from ldap3 import Server, Connection, SUBTREE, LEVEL, SYNC, ALL_ATTRIBUTES, ALL
from utils.secure_string import SecureString



def test_ad_con():
    server = Server('dc.abc.local', get_info=ALL)
    conn = Connection(server, 'konshin.av', 'P@$$w0rd',
                           auto_bind=True)
    conn.search('dc=abc,dc=local', '(objectclass=computer)')
    # for  i in conn.entries: print(i)
    return conn.entries

if __name__ == '__main__':
    pass