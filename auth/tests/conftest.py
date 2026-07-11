import os
from pathlib import Path

import psycopg2
import pytest
from dotenv import load_dotenv

from app.DataBase import DataBaseConnection

load_dotenv()


@pytest.fixture(scope="module")
def data_base_prep():
    conn = psycopg2.connect(
        dbname=os.getenv("dbname"),
        user=os.getenv("dbUser"),
        password=os.getenv("dbPassword"),
        host=os.getenv("dbHost"),
        port=os.getenv("dbPort"),
    )
    cur = conn.cursor()

    sql_path = Path(__file__).resolve().parent / "createdb.sql"
    with sql_path.open("r", encoding="utf-8") as file:
        comandos = file.read()

    cur.execute(comandos)
    conn.commit()
    yield

    cur.close()
    conn.close()


@pytest.fixture(scope="module", name="dbConn")
def create_conn(data_base_prep):
    dbConn = DataBaseConnection(
        dbname="auth_hospital",
        user="postgres",
        password="postgres",
        host="localhost",
        port=5432,
    )
    yield dbConn
    dbConn.clear()


@pytest.fixture(scope="module")
def real_user():
    return {
        "nome": "Ana Cardoso",
        "username": "med.cardoso",
        "password": "PseudoPEP2026!",
        "funcao": "MEDICO",
    }


    
    


