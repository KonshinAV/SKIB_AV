#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import base64
import json
import urllib3
from pprint import pprint

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class KscKlApi (object):

    def __init__(self, user, pwd, auto_connect=True):
        self.ksc_server = "https://ksc.abc.local:13299"
        self.api_request = ''
        self.url = f"{self.ksc_server}/api/"
        self.user = user
        self.password = pwd
        self.user = base64.b64encode(self.user.encode('utf-8')).decode("utf-8")
        self.password = base64.b64encode(self.password.encode('utf-8')).decode("utf-8")
        self.session = requests.Session()
        self.data = {}
        self.auth() if auto_connect else None
        self.common_headers = {'Content-Type': 'application/json', }

    def auth(self):
        api_request = 'login HTTP/1.1'
        auth_headers = {
            'Authorization': 'KSCBasic user="' + self.user + '", pass="' + self.password + '", internal="0"',
            'Content-Type': 'application/json',
        }
        response = self.session.post(url=f'{self.url}{api_request}',
                                     headers=auth_headers,
                                     data=self.data,
                                     verify=False)
        self.auth_status_code = response.status_code
        return response.status_code

    def get_packages(self):
        api_request = 'PackagesApi.GetPackages'
        response = self.session.post(url=f'{self.url}{api_request}',
                                     headers=self.common_headers,
                                     data=self.data,
                                     verify=False)
        return json.loads(response.text)['PxgRetVal']

    def get_shared_folder(self):
        response = self.session.post(url=f'{self.url}AdmServerSettings.GetSharedFolder',
                                     headers=self.common_headers,
                                     data=self.data,
                                     verify=False)
        return json.loads(response.text)['PxgRetVal']

    def get_search_result(self, strAccessor):
        url = self.ksc_server + "/api/v1.0/ChunkAccessor.GetItemsCount"
        data = {"strAccessor": strAccessor}
        response = self.session.post(url=url,
                                     headers=self.common_headers,
                                     data=json.dumps(data),
                                     verify=False)
        items_count = json.loads(response.text)['PxgRetVal']
        url = self.ksc_server + "/api/v1.0/ChunkAccessor.GetItemsChunk"
        data = {"strAccessor": strAccessor,
                "nStart": 0,
                "nCount": items_count}
        response = self.session.post(url=url,
                                     headers=self.common_headers,
                                     data=json.dumps(data),
                                     verify=False)
        results = json.loads(response.text)['pChunk']['KLCSP_ITERATOR_ARRAY']
        return results

    def get_manage_groups(self):
        data = {
            'wstrFilter': '',
            'vecFieldsToReturn': ['id',
                                  'name',
                                  'parentId',
                                  'autoRemovePeriod',
                                  'hostsNum',
                                  'creationDate',
                                  'KLGRP_HlfForceChildren',
                                  'grp_full_name',
                                  'KLVSRV_DN',
                                  'KLSRVH_SRV_DN'],
            'lMaxLifeTime': 10
        }
        response = self.session.post(url=f'{self.url}HostGroup.FindGroups',
                                     headers=self.common_headers,
                                     data=json.dumps(data),
                                     verify=False)
        strAccessor = json.loads(response.text)['strAccessor']
        return self.get_search_result(strAccessor)

    def get_hosts(self, wstrFilter=''):
        url = f"{self.ksc_server}/api/v1.0/HostGroup.FindHosts"
        data = {'wstrFilter': wstrFilter,
                "pParams": {"KLSRVH_SLAVE_REC_DEPTH": 1,
                            "KLGRP_FIND_FROM_CUR_VS_ONLY": 'false'},
                'vecFieldsToReturn': ['KLHST_WKS_FQDN',
                                      'KLHST_WKS_WINHOSTNAME',
                                      'KLHST_WKS_DNSNAME',
                                      'KLHST_WKS_GROUPID',
                                      'name',
                                      'KLHST_WKS_HOSTNAME',
                                      'KLHST_WKS_STATUS',
                                      'KLHST_WKS_OS_NAME',
                                      'HST_VM_VDI',
                                      'KLHST_WKS_NAG_VERSION',
                                      'KLHST_WKS_RTP_AV_VERSION',
                                      'KLSRVH_SRV_DN'],
                'lMaxLifeTime': 10}
        response = self.session.post(url=url,
                                     headers=self.common_headers,
                                     data=json.dumps(data),
                                     verify=False)
        strAccessor = json.loads(response.text)['strAccessor']
        return self.get_search_result(strAccessor)

    def get_hosts_async(self, wstrFilter=''):
        url = f"{self.ksc_server}/api/v1.0/HostGroup.FindHostsAsync"
        data = {'wstrFilter': wstrFilter,
                'vecFieldsToReturn': ['KLHST_WKS_FQDN',
                                      'KLHST_WKS_WINHOSTNAME',
                                      'KLHST_WKS_DNSNAME',
                                      'KLHST_WKS_GROUPID',
                                      'name'],
                'pParams': {'KLSRVH_SLAVE_REC_DEPTH': 1},
                'lMaxLifeTime': 10
                }
        response = self.session.post(url=url,
                                     headers=self.common_headers,
                                     data=json.dumps(data),
                                     verify=False)
        strRequestId = json.loads(response.text)['strRequestId']
        pprint(strRequestId)
        strAccessor = self.find_hosts_async_get_accessor(strRequestId=strRequestId)
        pprint(strAccessor)
        # pprint(strRequestId)
        # pprint(self.get_search_result(strAccessor))
        # return  strRequestId

    def find_hosts_async_get_accessor(self, strRequestId):
        url = f"{self.ksc_server}/api/v1.0/HostGroup.FindHostsAsyncGetAccessor"
        data = {'strRequestId': strRequestId}
        response = self.session.post(url=url,
                                     headers=self.common_headers,
                                     data=json.dumps(data),
                                     verify=False)
        strAccessor = json.loads(response.text)
        return strAccessor

    def async_action_state(self):
        pass

    def get_child_servers(self):
        url = f"{self.ksc_server}/api/v1.0/ServerHierarchy.GetChildServers"
        data = {'nGroupId': -1}
        response = self.session.post(url=url,
                                     headers=self.common_headers,
                                     data=json.dumps(data),
                                     verify=False)
        return json.loads(response.text)['PxgRetVal']

    def get_static_info (self):
        url = f"{self.ksc_server}/api/v1.0/HostGroup.GetStaticInfo"
        data = {"pValues": []}
        response = self.session.post(url=url,
                                     headers=self.common_headers,
                                     data=json.dumps(data),
                                     verify=False)
        return json.loads(response.text)['PxgRetVal']

class HostGroupe (KscKlApi):
    def find_hosts_async_get_accessor(self, strRequestId):
        pass

if __name__ == '__main__':
    pass
