from utils import adtools, filestools, secure_string
from pprint import pprint


if __name__ == '__main__':
    DC_SETTINGS = filestools.json_dump_read('cfg\DC.json')
    DC_SETTINGS["pwd"] = secure_string.decoding(DC_SETTINGS["spwd"])
    abc_domain = adtools.ActiveDirectory(dc_server_name=DC_SETTINGS["server_name"],
                                         dc_domain_name=DC_SETTINGS["domain_name"],
                                         dc_user=DC_SETTINGS["user"],
                                         dc_pwd=DC_SETTINGS["pwd"],
                                         dc_root=DC_SETTINGS["root"])


    pass