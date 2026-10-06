import psycopg2

# Database connection configurations
DB_HOST = "localhost"
DB_USER = "postgres"
DB_PASS = "@A5+m14-E1*n13/"  # Change this to your real PostgreSQL password!
DB_PORT = "5432"

def init_postgres():
    # 1. Connect to default postgres database to create our new project database
    conn = psycopg2.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, port=DB_PORT)
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Create the Capstone database if it doesn't exist
    cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'capstone_locations';")
    exists = cursor.fetchone()
    if not exists:
        cursor.execute("CREATE DATABASE capstone_locations;")
        print(" Created database 'capstone_locations'")
    
    cursor.close()
    conn.close()

    # 2. Connect directly to the new database to construct tables
    conn = psycopg2.connect(dbname="capstone_locations", host=DB_HOST, user=DB_USER, password=DB_PASS, port=DB_PORT)
    cursor = conn.cursor()
    
    print("Building normalized PostgreSQL tables for the Capstone Project...")

    # States Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS states (
            id SERIAL PRIMARY KEY,
            state_name VARCHAR(100) UNIQUE NOT NULL
        );
    ''')
    
    # Districts Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS districts (
            id SERIAL PRIMARY KEY,
            state_id INTEGER NOT NULL REFERENCES states(id) ON DELETE CASCADE,
            district_name VARCHAR(100) NOT NULL,
            CONSTRAINT unique_state_district UNIQUE(state_id, district_name)
        );
    ''')
    
    # Sub-Districts Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sub_districts (
            id SERIAL PRIMARY KEY,
            district_id INTEGER NOT NULL REFERENCES districts(id) ON DELETE CASCADE,
            sub_district_name VARCHAR(100) NOT NULL,
            CONSTRAINT unique_district_sub UNIQUE(district_id, sub_district_name)
        );
    ''')
    
    # Villages Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS villages (
            id SERIAL PRIMARY KEY,
            sub_district_id INTEGER NOT NULL REFERENCES sub_districts(id) ON DELETE CASCADE,
            village_name VARCHAR(150) NOT NULL,
            pincode VARCHAR(20)
        );
    ''')
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Production PostgreSQL schema generated successfully!")

if __name__ == "__main__":
    init_postgres()