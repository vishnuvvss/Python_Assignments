import psycopg2
import logging
from psycopg2 import sql, OperationalError, IntegrityError

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def get_connection():
    """Establish and return a PostgreSQL connection."""
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        logging.info("Database connection established successfully.")
        return conn
    except OperationalError as e:
        logging.error(f"Database connection failed: {e}")
        return None

def create_users_table():
    """Create the 'users' table if it doesn't already exist."""
    conn = get_connection()
    if not conn:
        return

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(50) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL
                );
            """)
            conn.commit()
            logging.info("Users table created successfully.")
            print("Users table created successfully.")
    except Exception as e:
        logging.error(f"Error creating table: {e}")
        print("Error creating table:", e)
    finally:
        conn.close()

def create_user(name, email):
    """Insert a user safely with duplicate protection."""
    conn = get_connection()
    if not conn:
        return

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO users (name, email)
                VALUES (%s, %s)
                ON CONFLICT (email) DO NOTHING;
            """, (name, email))
            conn.commit()
            logging.info(f"User inserted successfully: {name} ({email})")
            print(f"User '{name}' inserted successfully.")
    except IntegrityError as e:
        logging.warning(f"Duplicate user insertion attempt: {email}")
        print(f"User with email '{email}' already exists.")
    except Exception as e:
        logging.error(f"Insert error: {e}")
        print("Insert error:", e)
    finally:
        conn.close()

def get_users():
    """Fetch and return all user records."""
    conn = get_connection()
    if not conn:
        return []

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users ORDER BY id;")
            rows = cursor.fetchall()
            logging.info(f"Fetched {len(rows)} users from database.")
            return rows
    except Exception as e:
        logging.error(f"Read error: {e}")
        print("Read error:", e)
        return []
    finally:
        conn.close()

def main():
    """Main execution block."""
    try:
        create_users_table()
        create_user("Karthik", "karthik@gmail.com")
        create_user("Vikram", "vikramvikky@gmail.com")

        users = get_users()
        print("\nAll users:")
        for u in users:
            print(u)
    except Exception as e:
        logging.critical(f"Unexpected error in main(): {e}")
        print("Unexpected error:", e)

if __name__ == "__main__":
    main()