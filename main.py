import sqlite3 as sql
import pandas as pd
import uuid

DATA_PATH = "data"

create_table_query = '''
CREATE TABLE IF NOT EXISTS Users (
    username TEXT PRIMARY KEY,
    password TEXT,
    email TEXT,
    balance REAL
);
'''

def all_records():
    users_connection = sql.connect(f"{DATA_PATH}/users.db")
    users_cursor = users_connection.cursor()

    select_query = "SELECT * FROM Users;"

    return pd.read_sql_query(select_query, users_connection)

def add_user(username: str, password: str, email: str):
    users_connection = sql.connect(f"{DATA_PATH}/users.db")
    users_cursor = users_connection.cursor()

    users_cursor.execute(create_table_query)

    insert_query = '''
    INSERT INTO Users (username, password, email, balance)
    VALUES (?, ?, ?, ?);
    '''

    user_data = (username, password, email, 0)
    users_cursor.execute(insert_query, user_data)

    users_connection.commit()

    users_connection.close()

def user_exists_email(email: str):
    users_connection = sql.connect(f"{DATA_PATH}/users.db")
    users_cursor = users_connection.cursor()

    users_cursor.execute(create_table_query)

    get_query = '''
    SELECT * FROM Users WHERE email = ?;
    '''

    users_cursor.execute(get_query, (email,))

    users = users_cursor.fetchall()

    return len(users) > 0

def get_user(email: str, password: str):
    users_connection = sql.connect(f"{DATA_PATH}/users.db")
    users_cursor = users_connection.cursor()

    users_cursor.execute(create_table_query)

    get_query = '''
    SELECT * FROM Users WHERE email = ?;
    '''

    users_cursor.execute(get_query, (email,))

    users = users_cursor.fetchall()

    for user in users:
        if user[2] == email and user[1] == password:
            return user

    return None

def update_balance(email: str, new_balance: float):
    users_connection = sql.connect(f"{DATA_PATH}/users.db")
    users_cursor = users_connection.cursor()

    users_cursor.execute(create_table_query)

    update_query = '''
    UPDATE Users 
    SET balance = ? 
    WHERE email = ?;
    '''

    users_cursor.execute(update_query, (new_balance, email))

print(all_records())

print("-" * 65, "\n\n")

#update_balance("timbob@example.com", 100.0)