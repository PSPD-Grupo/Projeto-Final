SECRET = "DT4xMpG3kn44CsQ1ijgTjrWftPTU3AQ9+jmSNT/4vUs="


class UserNotFoundError(Exception):
    """Levantada quando um username não existe no repositório."""
    def __init__(self, username: str):
        self.username = username
        super().__init__(f"usuário '{username}' não encontrado")


class InMemoryUserRepository:
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