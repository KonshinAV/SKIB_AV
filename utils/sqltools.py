import pyodbc
from pprint import pprint
import numpy as np
from utils import filestools

def KscExtendedStatusAsSList (key_int_status):
    key_bin_status = list(bin(key_int_status).split('b')[1][::-1])
    key_list_status = []
    dict_host_key_status = {}
    for i in range(len(key_bin_status)):dict_host_key_status.update({i: key_bin_status[i]})
    dict_extended_key_str_status = {0: 'Host with Network Agent installed is online but network agent is inactive',
                                    1: 'Anti-virus application is installed but real-time protection is not running',
                                    2: 'Anti-virus application is installed but not running',
                                    3: 'Number of viruses detected is too much',
                                    4: 'Anti-virus application is installed but real-time protection status differs from one set by the security administrator',
                                    5: 'Anti-virus application is not installed',
                                    6: 'Full scan for viruses performed too long ago',
                                    7: 'Anti-virus bases were updated too long ago',
                                    8: 'Network agent is inactive too long',
                                    9: 'Old license',
                                    10: 'Number of uncured objects is too much',
                                    11: 'Reboot is required',
                                    12: 'Incompatible applications are installed on the computer',
                                    13: 'There is at least one unfixed vulnerability on the computer',
                                    14: 'Search for Windows updates has not been launched for a long time',
                                    15: 'Encryption status is not compliant',
                                    16: 'Mobile device settings are not compliant',
                                    17: 'There is at least one unprocessed incident',
                                    18: '18 Status Code',
                                    19: 'The device is running out of disk space'
                                    }
    for bit in dict_host_key_status:
        if dict_host_key_status[bit] == '1':
            key_list_status.append(dict_extended_key_str_status[bit])
    return key_list_status

class KlSqlServer:

    def __init__(self, server, database, username, pwd, autoconnect = True, trusted_connection = True):
        self.server = server
        self.database = database
        self.username = username
        self.pwd = pwd
        self.cursor = None
        if autoconnect: self.connect_db()


    def connect_db(self, sql_driver = '{SQL Server}'):
        conn = pyodbc.connect (f"DRIVER={sql_driver};SERVER={self.server};PORT=1433;DATABASE={self.database};UID={self.username};PWD={self.pwd}")
        self.cursor = conn.cursor()
        pass

    def get_ksc_tasks (self):
        self.cursor.execute ('''
                        SELECT [task_id]
                          ,[task_name]
                          ,[product_name]
                          ,[product_version]
                          ,[component_name]
                          ,[task_display_name]
                          ,[group_id]
                          ,[nVServerId]
                          ,[strClusterId] FROM v_akpub_tsk_task
                        ''')
        return self.cursor.fetchall()

    def get_test_data (self):
        self.cursor.execute('''
            SELECT v_akpub_adm_group.wstrName,
                v_akpub_host.wstrDnsName,
                v_akpub_host.wstrDnsDomain,
                v_akpub_host.wstrWinDomain,
                v_akpub_hst_prdstate.tmAvbasesDate,
                v_akpub_host.nLastRtpState,
                v_akpub_host_status.nStatus,
                v_akpub_hst_prdstate.wstrProductBuildNumber,
                v_akpub_host.nStatus,
                v_akpub_host_status.nStatusMask
            FROM v_akpub_host 
            INNER JOIN v_akpub_adm_group ON v_akpub_host.nGroup = v_akpub_adm_group.nId
            INNER JOIN v_akpub_host_status ON v_akpub_host_status.nId = v_akpub_host.nId
            INNER JOIN v_akpub_hst_prdstate ON v_akpub_hst_prdstate.nHost = v_akpub_host_status.nId
            WHERE v_akpub_adm_group.nParentId != 1
            ORDER BY v_akpub_host.wstrDisplayName DESC
            ''')
        return self.cursor.fetchall()

    def get_data_per_host (self, host_name):
        self.cursor.execute(f"""
                SELECT	v_akpub_host.nId,
                        v_akpub_adm_group.wstrName,
                        v_akpub_host.wstrDnsName,
                        v_akpub_host.wstrDisplayName,
                        v_akpub_host.wstrDnsDomain,
                        v_akpub_host.wstrWinDomain,
                        v_akpub_host.tmLastVisible,
                        v_akpub_host.tmLastUpdate,
                        v_akpub_host.tmLastFullScan,
                        v_akpub_host.tmLastNagentConnected,
                        v_akpub_host.nLastRtpState,
                        v_akpub_host_status.nStatus,
                        v_akpub_host.nStatus,
                        v_akpub_host_status.nStatusMask,
                        v_akpub_hst_prdstate.wstrProductDisplayName,
                        v_akpub_hst_prdstate.wstrProductBuildNumber,
                        v_akpub_hst_prdstate.nProduct
                FROM v_akpub_host
                FULL JOIN v_akpub_adm_group ON v_akpub_host.nGroup = v_akpub_adm_group.nId
                FULL JOIN v_akpub_host_status ON v_akpub_host_status.nId = v_akpub_host.nId
                FULL JOIN v_akpub_hst_prdstate ON v_akpub_hst_prdstate.nHost = v_akpub_host.nId
                WHERE v_akpub_adm_group.nParentId != 1 AND
                v_akpub_host.wstrDnsName = '{host_name}'
                            """)
        query_result = self.cursor.fetchall()
        # print(len(query_result))
        # pprint(query_result)
        one_count = dict({})
        for record in query_result:
            if not record[0] in one_count.keys():
                one_count[record[0]] = dict({})
                one_count[record[0]]['adm_group.wstrName'] = record[1]
                one_count[record[0]]['host.wstrDnsName'] = record[2]
                one_count[record[0]]['host.wstrDisplayName'] = record[3]
                one_count[record[0]]['host.wstrDnsDomain'] = record[4]
                one_count[record[0]]['host.wstrWinDomain'] = record[5]
                one_count[record[0]]['host.tmLastVisible'] = record[6]
                one_count[record[0]]['host.tmLastUpdate'] = record[7]
                one_count[record[0]]['host.tmLastFullScan'] = record[8]
                one_count[record[0]]['host.tmLastNagentConnected'] = record[9]
                one_count[record[0]]['host.nLastRtpState'] = record[10]
                if record[11] == 0:
                    one_count[record[0]]['host_status.nStatus'] = 'OK'
                elif record[11] == 1:
                    one_count[record[0]]['host_status.nStatus'] = 'Critical'
                elif record[11] == 2:
                    one_count[record[0]]['host_status.nStatus'] = 'Warning'
                one_count[record[0]]['host.nStatus'] = record[12]
                one_count[record[0]]['host_status.nStatusMask'] = record[13]
                # Расшифровка статуса в читаемый вид
                one_count[record[0]]['host_status.wstrStatusMask'] = ', '.join(KscExtendedStatusAsSList(one_count[record[0]]['host_status.nStatusMask']))

            if record[-1] == 2: # Если продукт это Агент администрировния, то проставляем значения Nagent
                one_count[record[0]]['host.NagentVersion'] = record[-2]
                one_count[record[0]]['host.NagentDescription'] = record[-3]
            elif record[-1] != 1 and record[-1] != 2: # Если продукт не Агент администрирования или не KSC, то проставляем значения для AV
                one_count[record[0]]['host.AvVersion'] = record[-2]
                one_count[record[0]]['host.AvDescription'] = record[-3]

            # Если после выгрузки не сформировался ключ AvVersion - нет АВЗ на устройстве
            # Добавляем ключ принудительно с пустым значением
            if not 'host.AvVersion' in one_count[record[0]].keys():
                one_count[record[0]]['host.AvVersion'] = None
                one_count[record[0]]['host.AvDescription'] = None

            # Если после выгрузки не сформировался ключ NagentVersion - нет агента администрирования на устройстве
            # Нет вообще никакой информации по хосту, но запись является управляемой
            # Добавляем ключ принудительно с пустым значением
            if not 'host.NagentVersion' in one_count[record[0]].keys():
                one_count[record[0]]['host.NagentVersion'] = None
                one_count[record[0]]['host.NagentDescription'] = None

            if one_count[record[0]]['adm_group.wstrName'] != None and one_count[record[0]]['host.NagentVersion'] == None:
                one_count[record[0]]['host_status.nStatus'] = 'Critical'
                one_count[record[0]]['host_status.wstrStatusMask'] = 'NagentNotInstalled'
        return one_count

if __name__ == '__main__':

    pass
