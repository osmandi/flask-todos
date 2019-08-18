import sqlite3

DATABASE = './database.db'



'''
c.execute('SELECT')
rows = c.fetchall()
conn.close()
'''

def get_users():

    try:
        conn, c = init_database()

        c.execute('SELECT * FROM users')
        response = c.fetchall()
        return response
    finally:
        close_conexion(conn)

def get_user(user_id):
    try:
        conn, c = init_database()
        sql_query = '''SELECT name, password FROM users
        WHERE name = "{}"'''.format(user_id)
        c.execute(sql_query)
        return c.fetchall()
    finally:
        close_conexion(conn)

def get_todos(username):
    try:
        conn, c = init_database()
        sql_query = '''SELECT description FROM todos 
        INNER JOIN users ON users.id = todos.user_id 
        WHERE users.name = "{}"'''.format(username)
        c.execute(sql_query)
        response = c.fetchall()
        return response
    finally:
        close_conexion(conn)

# Open Database
def init_database():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    return (conn, c)

# Close Database
def close_conexion(connection):
   connection.close()

