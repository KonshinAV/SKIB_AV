from utils import adtools, filestools, secure_string
from utils import sqltools, openapi
from pprint import pprint
import numpy as np


if __name__ == '__main__':
    DC_SETTINGS = filestools.json_dump_read('cfg\DC.json')
    DC_SETTINGS['abc.local']["pwd"] = secure_string.decoding(DC_SETTINGS['abc.local']["spwd"])

    KSC_SETTINGS = filestools.json_dump_read('cfg\ksc.json')
    KSC_SETTINGS['ksc_main']["pwd"] = secure_string.decoding(KSC_SETTINGS['ksc_main']["spwd"])

    abc_domain = adtools.ActiveDirectory(server_name=DC_SETTINGS['abc.local']["server_name"],
                                         domain_name=DC_SETTINGS['abc.local']["domain_name"],
                                         username=DC_SETTINGS['abc.local']["user"],
                                         pwd=DC_SETTINGS['abc.local']["pwd"],
                                         root=DC_SETTINGS['abc.local']["root"])

    ksc_sql = sqltools.KlSqlServer(server=KSC_SETTINGS['ksc_main']['db_server_name'],
                               database=KSC_SETTINGS['ksc_main']['db_name'],
                               username=KSC_SETTINGS['ksc_main']['user'],
                               pwd=KSC_SETTINGS['ksc_main']['pwd'])

    ksc_api = openapi.KscKlApi(user='automation_user',
                              pwd=KSC_SETTINGS['ksc_main']['pwd'])
    print(ksc_sql.get_ksc_tasks())


    # for i in child_serv: print(i)