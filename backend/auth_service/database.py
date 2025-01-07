from psycopg2 import pool

# Database connection pool
DATABASE_CONFIG = {
    'dbname': 'user_services',
    'user': 'postgres',
    'password': 'root',
    'host': '192.168.0.100',
    'port': '5432'
}

connection_pool = pool.SimpleConnectionPool(
    1, 20,
    dbname=DATABASE_CONFIG['dbname'],
    user=DATABASE_CONFIG['user'],
    password=DATABASE_CONFIG['password'],
    host=DATABASE_CONFIG['host'],
    port=DATABASE_CONFIG['port']
)

def get_db_connection():
    if connection_pool:
        return connection_pool.getconn()

def release_db_connection(conn):
    if connection_pool:
        connection_pool.putconn(conn)
