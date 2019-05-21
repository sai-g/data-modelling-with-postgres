import psycopg2
from sql_queries import create_table_queries, drop_table_queries

# database info
STUDENT_DB_NAME = "studentdb"
SPARKIFY_DB_NAME = "sparkifydb"
USER_NAME = "student"
PASSWORD = "student"
HOST_NAME = "127.0.0.1"

# SQL statements
DROP_DB = "DROP DATABASE IF EXISTS {}"
CREATE_DB = "CREATE DATABASE {} WITH ENCODING 'utf8' TEMPLATE template0"

CONNECT_TO_DB = "host={} dbname={} user={} password={}"


def create_database():
    """ function to create database and to return db cursor and connection """
    global cur
    try:
        # connect to default database
        conn = psycopg2.connect(CONNECT_TO_DB.format(HOST_NAME, STUDENT_DB_NAME, USER_NAME, PASSWORD))
        conn.set_session(autocommit=True)
        cur = conn.cursor()
    except:
        print("Could not connect to {} database".format(STUDENT_DB_NAME))
        raise ConnectionError("Error in connecting to database")

    try:
        # create sparkify database with UTF8 encoding
        cur.execute(DROP_DB.format(SPARKIFY_DB_NAME))
        cur.execute(CREATE_DB.format(SPARKIFY_DB_NAME))
        # close connection to default database
        conn.close()
    except:
        print("Error in executing drop/create sql statements")

    try:
        # connect to sparkify database
        conn = psycopg2.connect(CONNECT_TO_DB.format(HOST_NAME, SPARKIFY_DB_NAME, USER_NAME, PASSWORD))
        cur = conn.cursor()
    except:
        print("Could not connect to {} database".format(SPARKIFY_DB_NAME))

    return cur, conn


def drop_tables(cur, conn):
    """ This function iterates over drop table queries to execute each sql statement """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """ This function iterates over create table queries to execute each sql statement """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    cur, conn = create_database()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
