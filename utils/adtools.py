from ldap3 import Server, Connection, SUBTREE, LEVEL, SYNC, ALL_ATTRIBUTES, ALL

class ActiveDirectory:
    def __init__(self, dc_server_name, dc_root, dc_user, dc_pwd, dc_domain_name, dc_auto_connection = True):
        self.dc_server_name = dc_server_name
        self.dc_root = dc_root
        self.dc_user = dc_user
        self.dc_pwd = dc_pwd
        self.dc_domain_name = dc_domain_name
        self.dc_connection = self.create_connection() if dc_auto_connection is True else None

    def create_connection (self):
        server = Server(self.dc_server_name, get_info=ALL)
        conn = Connection(server, user = self.dc_user, password = self.dc_pwd, auto_bind=True)
        return conn


    def get_all_computers(self):
        pass

    def get_computer (self, computer_name,  attrs):
        self.computer_name = computer_name
        self.attrs = attrs
        pass

    def get_computers_in_ou (self, ou_name):
        self.ou_name = ou_name
        pass

if __name__ == '__main__':
    pass