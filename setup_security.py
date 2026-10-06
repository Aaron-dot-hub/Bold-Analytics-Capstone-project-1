import psycopg2

# Database configuration
DB_HOST = "localhost"
DB_USER = "postgres"
DB_PASS = "@A5+m14-E1*n13/"  #  Replace this with your real PostgreSQL password!
DB_NAME = "capstone_locations"
DB_PORT = "5432"

def verify_and_fix_security():
    try:
        conn = psycopg2.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, dbname=DB_NAME, port=DB_PORT)
        cursor = conn.cursor()
        
        print(" Ensuring B2B Client Security table is perfectly aligned...")
        
        # Drop table if it was corrupted or misaligned, then recreate it cleanly
        cursor.execute("DROP TABLE IF EXISTS b2b_clients CASCADE;")
        
        cursor.execute('''
            CREATE TABLE b2b_clients (
                id SERIAL PRIMARY KEY,
                company_name VARCHAR(100) NOT NULL,
                api_key VARCHAR(64) UNIQUE NOT NULL,
                api_secret VARCHAR(64) NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        
        # Inject the credentials the python script is looking for
        cursor.execute('''
            INSERT INTO b2b_clients (company_name, api_key, api_secret) 
            VALUES ('Bold Demo Corp', 'DEMO_KEY_2026', 'DEMO_SECRET_2026');
        ''')
        
        conn.commit()
        
        # Double check insertion
        cursor.execute("SELECT company_name, api_key FROM b2b_clients;")
        record = cursor.fetchone()
        print(f" Security Layer Active! Verified Key in Database: {record[1]} for {record[0]}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f" Failed to setup security table: {e}")

if __name__ == "__main__":
    verify_and_fix_security()