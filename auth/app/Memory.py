import sys, os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.MemoryInterface import *




class InMemoryUserRepository(MemoryInterface):
    """Repositório simples em memória, só para exemplo/testes."""
 
    def __init__(self):
        self._users = {}
        self.permission = {}
        self._loged_in = {}
 
    def create_user(self, username: str, password: str, permission: tuple):
        self._users[username] = password
        self.permission[username] = permission
        self._loged_in[username] = False
 
    def __getitem__(self, username):
        return self.permission[username]

    def getPermissions(self, username):
        return self.permission[username]
 
    def check_credentials(self, username: str, password: str) -> bool:
        return self._users.get(username) == password
    
    def check_user_exists(self, username):
        return username in self._users.keys()
    
    def login(self, username):
        self._loged_in[username] = True
    
    def logout(self, username):
        self._loged_in[username] = False
    
    def isLoged_in(self, username):
        return self._loged_in[username]
 
    def clear(self):
        self._users.clear()
        self.permission.clear()
        self._loged_in.clear()