import pyodbc
from abc import ABC

from src.configuration import Credenciais


class Database(ABC):
    def __init__(self, dbname):
        self.dbname = dbname

    def exec_command(self, sql):
        try:
            conn = pyodbc.connect(Credenciais.POSTGRESQL, autocommit=True)
            cursor = conn.cursor()
            cursor.execute(sql)
            cursor.close()
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f'[database.py] Error: {e}')
            return False

    def exec_query(self, sql):
        try:
            conn = pyodbc.connect(Credenciais.POSTGRESQL, autocommit=True)
            cursor = conn.cursor()
            cursor.execute(sql)
            res = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
            cursor.close()
            conn.commit()
            conn.close()
            return res
        except Exception as e:
            print(f'Error: {e}')
            return {}
