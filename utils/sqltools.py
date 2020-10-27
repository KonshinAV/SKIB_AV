import pyodbc
from pprint import pprint
import numpy as np


class KlSqlServer:

    def __init__(self, server, database, username, pwd, autoconnect = True):
        self.server = server
        self.database = database
        self.username = username
        self.pwd = pwd
        self.cursor = None
        if autoconnect: self.connect_db()


    def connect_db(self, sql_driver = '{SQL Server Native Client 11.0}'):
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
        rows = self.cursor.fetchall()
        return np.array(rows)

    def create_db(self):
        pass

    def drop_db(self):
        pass



if __name__ == '__main__':

    pass
