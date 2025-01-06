from psycopg2 import pool

# Database configuration
DATABASE_CONFIG = {
    'dbname': 'expense_service',
    'user': 'postgres',
    'password': 'root',
    'host': '192.168.0.100',
    'port': '5432'
}

# Connection pool
connection_pool = pool.SimpleConnectionPool(
    1, 20,
    dbname=DATABASE_CONFIG['dbname'],
    user=DATABASE_CONFIG['user'],
    password=DATABASE_CONFIG['password'],
    host=DATABASE_CONFIG['host'],
    port=DATABASE_CONFIG['port']
)

def get_db_connection():
    """Retrieve a connection from the pool."""
    if connection_pool:
        return connection_pool.getconn()

def release_db_connection(conn):
    """Release a connection back to the pool."""
    if connection_pool:
        connection_pool.putconn(conn)


