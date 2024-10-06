import sqlite3

def db_start(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print('db_start-error: ', e)
    return conn

def create_tables(conn):
    sql_query_1 = '''
    CREATE TABLE IF NOT EXISTS filepaths (
        pathId INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        url TEXT NOT NULL,
        desc TEXT
    );'''
    sql_query_2 = '''
    CREATE TABLE IF NOT EXISTS envs (
        envId INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        value TEXT NOT NULL,
        pathId INTEGER,
        FOREIGN KEY (pathId) REFERENCES filepaths(pathId)
    );'''
    try:
        cursor = conn.cursor()
        cursor.execute(sql_query_1)
        cursor.execute(sql_query_2)
    except sqlite3.Error as e:
        print('create_tables-error: ', e)


def get_filepaths_from_db(conn):
    select_query = '''
    SELECT name FROM filepaths;
    '''
    try:
        cursor = conn.cursor()
        cursor.execute(select_query)
        filepaths = cursor.fetchall()
    except sqlite3.Error as e:
        print(e)
    return [row[0] for row in filepaths]


def get_filepath_details(conn, name):
    select_query = '''
    SELECT name, url, desc FROM filepaths WHERE name = ?;
    '''
    try:
        cursor = conn.cursor()
        cursor.execute(select_query, (name,))
        details = cursor.fetchone()  # Hakee vain yhden tietueen
    except sqlite3.Error as e:
        print(e)
    return details
    
    
def add_filepath_to_db(conn, name, url, desc):
    sql_query_3 = '''
    INSERT INTO filepaths (name, url, desc) VALUES (?, ?, ?);
    '''
    try:
        cursor = conn.cursor()
        cursor.execute(sql_query_3, (name, url, desc))
        conn.commit()
    except sqlite3.Error as e:
            print(e)


def delete_filepath_from_db(conn, pathId):
    delete_filepath_query = '''
    DELETE FROM filepaths WHERE pathId = ?;
    '''
    try:
        cursor = conn.cursor()
        cursor.execute(delete_filepath_query, pathId)
    except sqlite3.Error as e:
        print(e)


def update_filepath_in_db(conn, pathId, name, url):
    update_filepath_query = '''
    UPDATE filepaths SET name = ?, url = ? WHERE pathId = ?);
    '''
    try:
        cursor = conn.cursor()
        cursor.execute(update_filepath_query, name, url, pathId)
    except sqlite3.Error as e:
        print(e)