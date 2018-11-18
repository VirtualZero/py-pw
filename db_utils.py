import os
import sqlite3

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'pwmanager.sqlite3')

def db_connect(db_path=DEFAULT_PATH):
    db_connection = sqlite3.connect(db_path, isolation_level=None)
    db_cursor = db_connection.cursor()
    return db_cursor

def create_new_db():
    db_cursor = db_connect()

    credentials_sql = """CREATE TABLE credentials (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
            accountname text NOT NULL UNIQUE,
            username text NOT NULL,
            password text NOT NULL
        )                  
    """

    db_cursor.execute(credentials_sql)

def add_new_creds(account_name, username, pw):
    db_cursor = db_connect()
    creds_sql = """INSERT INTO credentials (accountname, username, password) VALUES (?, ?, ?)"""
    db_cursor.execute(creds_sql, (account_name, username, pw))

def view_all_creds():
    db_cursor = db_connect()
    view_sql = """SELECT * FROM credentials"""
    db_cursor.execute(view_sql)
    print("\n")

    for account in db_cursor.fetchall():
        print(f"{account[0]}\t{account[1]}")
        print(f"\t{account[2]}")
        print(f"\t{account[3]}\n")

def count_creds():
    db_cursor = db_connect()
    db_cursor.execute("SELECT count(*) FROM credentials")
    return db_cursor.fetchone()[0]

def update_creds_by_id(id, field, new_cred):
    db_cursor = db_connect()
    update_sql = f"UPDATE credentials SET {field} = ? WHERE id = ?"
    db_cursor.execute(update_sql, (new_cred, id))

def update_creds_by_account_name(account_name, field, new_cred):
    db_cursor = db_connect()
    update_sql = f"UPDATE credentials SET {field} = ? WHERE accountname = ?"
    db_cursor.execute(update_sql, (new_cred, account_name))