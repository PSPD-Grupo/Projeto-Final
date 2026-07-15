import psycopg2
import os, sys
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.MemoryInterface import *

from dotenv import load_dotenv, dotenv_values 
    # loading variables from .env file
load_dotenv()

TEMPLATE_FUNCAO = {
    "MEDICO": ["FULL"],
    "PESQUISADOR": ["AGREGATED"],
    "ESTAGIARIO": ["PARTIAL"]
}

class DataBaseConnection(MemoryInterface):
    def __init__(self, dbname=os.getenv("dbname"), user=os.getenv('dbUser'), 
               password=os.getenv('dbPassword'), host=os.getenv('dbHost'), port=os.getenv('dbPort')):
        print(dbname, user, password, host, port)
        self._conn = self.conect(dbname, user, password, host, port)
        self._cur = self._conn.cursor()


    def conect(self, dbname, user, password, host, port):
        return psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port,
        )

    def getPermissions(self,username):
        print('_'*50)
        print(self._cur, username)
        print('_'*50)

        if self.check_user_exists(username):
            self._cur.execute(
                """SELECT funcao FROM user_account WHERE username=%s;""", (username,)
            )
            funcao = self._cur.fetchall()[0][0]
            print(funcao, type(funcao))
            return TEMPLATE_FUNCAO[funcao]
        else:
            raise UserNotFoundError(username)


    
    def create_user(self, username: str, password: str, permission: tuple):
        pass
 
    def __getitem__(self, username):
        pass
 
    def check_credentials(self, username: str, password: str) -> bool:
        self._cur.execute(
            """
            SELECT user_id, username, nome, funcao
            FROM user_account
            WHERE username = %s
            AND password_hash = crypt(%s, password_hash);
            """,
            (username, password)
        )
        row = self._cur.fetchone()
        return row is not None
    
    def check_user_exists(self, username):
        self._cur.execute(
            """SELECT 1 FROM user_account WHERE username=%s;""", (username,)
        )
        row = self._cur.fetchone()
        return row is not None
    
 
    def clear(self):
        self._cur.close()
        self._conn.close()


if __name__=="__main__":
    db = DataBaseConnection()