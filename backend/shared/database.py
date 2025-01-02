import psycopg2
from psycopg2 import pool

DATABASE_CONFIG = {
    'dbname': 'expense_tracker',
    'user': 'postgres',
    'password': '9009',
    'host': 'localhost',
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
def test_db_connection():
    conn = None
    try:
        # Get a connection from the pool
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Execute a simple test query
        cursor.execute("SELECT 1;")
        result = cursor.fetchone()
        
        # Check if query returned the expected result
        if result and result[0] == 1:
            print("Database connection is successful.")
        else:
            print("Database connection test failed.")
        
        # Close the cursor
        cursor.close()
    except Exception as e:
        print("Error while testing database connection:", e)
    finally:
        # Release the connection back to the pool
        if conn:
            release_db_connection(conn)

# Call the test function
test_db_connection()


if __name__ == "__main__":
    test_db_connection()

