import pytest
from app.DataBase import DataBaseConnection
from app.Memory import UserNotFoundError

class TestDataBase:
    def test_database_conn(self):
        db = DataBaseConnection(
            dbname="auth_hospital", user="postgres", 
            password="postgres",host="localhost", port=5432
        )

        assert db is not None
    
    def test_check_credential_success(self, dbConn, real_user):
        logado = dbConn.check_credentials(real_user["username"], real_user["password"])
        assert logado is True
    
    def test_check_credential_wrong_password(self, dbConn, real_user):
        logado = dbConn.check_credentials(real_user["username"], "wrong_password")
        assert logado is False

    def test_check_credential_incorrect_user(self, dbConn):
        logado = dbConn.check_credentials("not real", "wrong_password")
        assert logado is False
    
    def test_check_user_exists_success(self, dbConn, real_user):
        existe = dbConn.check_user_exists(real_user["username"])
        assert existe is True
    
    def test_check_user_exists_incorrect_user(self, dbConn):
        existe = dbConn.check_user_exists("not a user")
        assert existe is False
    
    def test_getPermissions_success(self, dbConn, real_user):
        print(real_user["username"])
        permissoes = dbConn.getPermissions(real_user["username"])
        assert 'FULL' in permissoes
        assert 'PARTIAL' not in  permissoes
    
    def test_getPermission_fail_not_real_user(self, dbConn):
        with pytest.raises(UserNotFoundError):
            permissoes = dbConn.getPermissions("not a real user")
        
