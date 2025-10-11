import mysql.connector
from src import app

def get_db():
    return mysql.connector.connect(
        host= app.config['MYSQL_HOST'],
        database= app.config['MYSQL_DATABASE'],
        user= app.config['MYSQL_USER'],
        password= app.config['MYSQL_PASSWORD']
    )

def close_db(con):
    return con.close()


