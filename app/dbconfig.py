import mysql.connector

def dbConnection():
    conn = mysql.connector.connect(
        host="localhost",
        user="asibd",
        password="#asiBD12",
        database="monitoring_system"
    )

    return conn
