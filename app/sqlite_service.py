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
        sql_query = '''SELECT description, done, todos.id FROM todos 
        INNER JOIN users ON users.id = todos.user_id 
        WHERE users.name = "{}"'''.format(username)
        c.execute(sql_query)
        response = c.fetchall()
        return response
    finally:
        close_conexion(conn)

def user_put(user_data):
    try:
        conn, c = init_database()
        sql_query = '''INSERT INTO users(name, password) VALUES("{}", "{}")
        '''.format(user_data.username, user_data.password)
        c.execute(sql_query)
        conn.commit()

       
    finally:
        close_conexion(conn)

def put_todos(user_id, description, done):
    try:
        conn, c = init_database()
        sql_query='''INSERT INTO todos(user_id, description, done) 
        VALUES ((SELECT id FROM users WHERE name="{}"), "{}", "{}")'''.format(user_id, description, done)
        c.execute(sql_query)
        conn.commit()
    finally:
        close_conexion(conn)

def delete_todo(user_id, todo_id):
    try:
        conn, c = init_database()
        sql_query = '''DELETE FROM todos
        WHERE todos.id = "{}" AND user_id = (SELECT id FROM users WHERE users.name = "{}")
        '''.format(todo_id, user_id)
        c.execute(sql_query)
        conn.commit()
    finally:
        close_conexion(conn)

def update_todo(user_id, todo_id, done):
    try:
        conn, c = init_database()
        done = int(not(done))
        sql_query = '''UPDATE todos set done="{}"
        WHERE todos.id = "{}" AND user_id = (SELECT id FROM users WHERE users.name = "{}")
        '''.format(done, todo_id, user_id)
        c.execute(sql_query)
        conn.commit()
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

