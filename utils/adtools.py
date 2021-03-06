from ldap3 import Server, Connection, SUBTREE, LEVEL, ALL
from datetime import datetime
from utils import filestools, secure_string
from pprint import pprint

class ActiveDirectory:
    def __init__(self, server_name, root, username, pwd, domain_name, auto_connection = True):
        self.dc_server_name = server_name
        self.dc_root = root
        self.dc_user = username
        self.dc_pwd = pwd
        self.dc_domain_name = domain_name
        self.dc_connection = self.create_connection() if auto_connection is True else None

    def create_connection (self):
        '''
        Метод создания подключения к AD с использованием LDAP

        :return: Connection
        '''
        server = Server(self.dc_server_name, get_info=ALL)
        conn = Connection(server, user = self.dc_user, password = self.dc_pwd, auto_bind=True)
        return conn

    def get_computer (self, computer_name, find_criteria = 'CN'):
        '''
        Метод поиска записи типа Computer  в домене и сбора атрибутов записи.

        Поддерживаются следующие атрибуты:
         existInDomain:bool
         name:str
         displayName:str
         distinguishedName:str
         distinguishedName_reversed:str
         enabled:bool
         location:str
         dNSHostName:str
         lastLogoff:datetime/None
         lastLogon::datetime/None
         lastLogonTimestamp::datetime/None
         objectCategory:str
         objectClass:str
         objectSid:str
         OperatingSystem:str
         operatingSystemVersion:str
         sAMAccountName:str
         userAccountControl:int
         whenCreated::datetime/None
         whenChanged:datetime/None
         uptime:int/None

        :param computer_name:str: имя искомого устройства
        :find_criteria:
        :return:
        '''
        self.find_name = computer_name
        self.ad_attrs = ('name',
                         'distinguishedName',
                         'displayName',
                         'dNSHostName',
                         'lastLogoff',
                         'lastLogon',
                         'lastLogonTimestamp',
                         'objectCategory',
                         'objectClass',
                         'objectSid',
                         'OperatingSystem',
                         'operatingSystemVersion',
                         'sAMAccountName',
                         'userAccountControl',
                         'whenCreated',
                         'whenChanged',
                         )
        self.dc_connection.search(search_base=self.dc_root,
                                  search_filter=f"(&(objectCategory=Computer)({find_criteria}={computer_name}))",
                                  search_scope=SUBTREE,
                                  attributes=self.ad_attrs
                                  )
        entries  = self.dc_connection.entries
        ad_computer = {}
        if len(entries) == 0:
            # Возврат None если объект с именем не найден
            return  None
        else:
            entries = entries[0]
            ad_computer['existInDomain'] = True
            ad_computer['name'] = str(entries['name']).lower()
            ad_computer['distinguishedName'] = str(entries['distinguishedName']).lower()
            distinguishedName_reversed = str(entries['distinguishedName']).split(',')[::-1]
            ad_computer['distinguishedName_reversed'] = ','.join(distinguishedName_reversed)
            del distinguishedName_reversed[-1] # Удаление имени объекта из строки DN
            ad_computer['location'] = ','.join(distinguishedName_reversed)
            ad_computer['displayName'] = str(entries['displayName'])
            ad_computer['dNSHostName'] = str(entries['dNSHostName']).lower()
            ad_computer['lastLogoff'] = str(entries['lastLogoff']).lower()
            try:
                ad_computer['lastLogon'] = datetime.strptime(str(self.dc_connection.entries[0]['lastLogon'])[0:19],'%Y-%m-%d %H:%M:%S')
            except ValueError as ex:
                ad_computer['lastLogon'] = None
            try:
                ad_computer['lastLogonTimestamp'] = datetime.strptime(str(entries['lastLogonTimestamp'])[0:19],'%Y-%m-%d %H:%M:%S')
            except ValueError as ex:
                ad_computer['lastLogonTimestamp'] = None
            try:
                ad_computer['lastLogoff'] = datetime.strptime(str(entries['lastLogoff'])[0:19],'%Y-%m-%d %H:%M:%S')
            except ValueError as ex:
                ad_computer['lastLogoff'] = None
            ad_computer['objectCategory'] = str(entries['objectCategory'])
            ad_computer['objectClass'] = str(entries['objectClass'])
            ad_computer['objectSid'] = str(entries['objectSid'])
            ad_computer['operatingSystem'] = str(entries['operatingSystem'])
            ad_computer['operatingSystemVersion'] = str(entries['operatingSystemVersion'])
            ad_computer['sAMAccountName'] = str(entries['sAMAccountName'])
            ad_computer['userAccountControl'] = int(str(entries['userAccountControl']))
            try:
                ad_computer['whenCreated'] = datetime.strptime(str(entries['whenCreated'])[0:19],'%Y-%m-%d %H:%M:%S')
            except ValueError as ex:
                ad_computer['whenCreated'] = None
            try:
                ad_computer['whenChanged'] = datetime.strptime(str(entries['whenChanged'])[0:19],'%Y-%m-%d %H:%M:%S')
            except ValueError as ex:
                ad_computer['whenChanged'] = None
            ad_computer['enabled'] = False if int(str(entries['userAccountControl'])) == 4098 or \
                                              int(str(entries['userAccountControl'])) == 4130 else True
            try:
                time_delta = str(datetime.now() - ad_computer['lastLogonTimestamp'])
                ad_computer['uptime'] = int(time_delta[0:time_delta.index('day')]) if 'day' in time_delta else 0
            except TypeError as ex:
                ad_computer['uptime'] = None
        return ad_computer

    def get_computers_for_list(self, computers_list, find_criteria = 'CN'):
        '''
        Метод загрузки информации по списку устройств.
        :param computers_dict:list/tuple: Входной список записей, поиск по которым требуется выполнить
        :find_criteria:str: Критерий по которому требуется выполнить поиск, по умолчанию = 'CN'
        :return:dict: Словарь результатов, key = искомое значение, value = результат поиска по домену (dict/None)
        '''
        computers_dict = {pc:self.get_computer(pc, find_criteria) for pc in computers_list}
        return computers_dict

    def get_computers_in_ou (self, search_base='root'):

        '''
        Метод поиска записей типа Computer в домене по OU и всех его потомках.

        :param search_base: str/None: Принимается полный путь OU в нотации AD. 'OU=XXX,OU=XXX,DC=XXX,DC=XXX'
                            Если не задано, то будет использоваться корень домена, как значение по умолчанию.
        :return: Кортеж, состоящий из элементов - записей компьютеров и их атрибутов.
                Если в OU  ничего не будет найдено - вернется пустой кортеж.
                Если OU задан некорректно - вернется пустой кортеж. Будет выполнена попытся его поиска в AD.

        '''
        search_base = self.dc_root if search_base == 'root' else search_base
        entries = self.dc_connection.extend.standard.paged_search(search_base=search_base,
                                                                  search_filter=f'(&(ObjectCategory=Computer))',
                                                                  search_scope=SUBTREE,
                                                                  attributes=['name'],
                                                                  paged_size=5,
                                                                  generator=True
                                                                  )
        computers = (self.get_computer(record['attributes']['name']) for record in entries if 'attributes' in record.keys())
        return tuple(computers)

    def get_child_ou(self, organizational_unit):
        '''
        Метод получения OU-потомков относительно заданного OU на глубину равную 1 уровень (прямые потомки)
        :param organizational_unit:str:OrganizationalUnit в нотации ActiveDirectory
        :return:tuple: кортеж из distinguishedName с OU потомками
        '''
        self.ad_attrs = ('Name',
                         'distinguishedName')
        self.dc_connection.search(search_base=organizational_unit,
                                  search_filter=f"(&(objectClass=OrganizationalUnit)(Name=*))",
                                  search_scope=LEVEL,
                                  attributes=self.ad_attrs
                                  )
        units = (str(i.distinguishedName) for i in self.dc_connection.entries)
        return tuple(units)
        pass

    def get_ou_list_by_mask (self, search_mask):
        """
        Метод поиска OU в демене по маске имени OU
        Оборачивающие * не установлены по умолчанию.
        :param search_mask: str: Поисковая маска
        :return: turple: Кортеж из OU найденых OU
        """
        self.ad_attrs = ('Name',
                         'distinguishedName')
        self.dc_connection.search(search_base=self.dc_root,
                                  search_filter=f"(&(objectClass=OrganizationalUnit)(Name={search_mask}))",
                                  search_scope=SUBTREE,
                                  attributes=self.ad_attrs
                                  )
        units = (str(i.distinguishedName) for i in self.dc_connection.entries)
        return tuple(units)

if __name__ == '__main__':
    pass
