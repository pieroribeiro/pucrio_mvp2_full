import mysql.connector
from app.mysql_config import mysql_config

def connect_to_database():
    conn = mysql.connector.connect(**mysql_config())
    return conn, conn.cursor()