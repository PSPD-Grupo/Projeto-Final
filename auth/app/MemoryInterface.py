
from abc import ABC, abstractmethod

class MemoryInterface(ABC):
    @abstractmethod
    def create_user(self, username: str, password: str, permission: tuple):
        pass

    @abstractmethod
    def getPermissions(self,username):
        pass
 
    @abstractmethod
    def check_credentials(self, username: str, password: str) -> bool:
        pass
    
    @abstractmethod
    def check_user_exists(self, username):
        pass
    
    
    @abstractmethod
    def clear(self):
        pass

class UserNotFoundError(Exception):
    """Levantada quando um username não existe no repositório."""
    def __init__(self, username: str):
        self.username = username
        super().__init__(f"usuário '{username}' não encontrado")
