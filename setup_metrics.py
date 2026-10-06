import psycopg2

# Database connection credentials
DB_HOST = "localhost"
DB_USER = "postgres"
DB_PASS = "@A5+m14-E1*n13/"  #  Use your real PostgreSQL password!
DB_NAME = "capstone_locations"
DB_PORT = "5432"

def create_metrics_table():
    try:
        conn = psycopg2.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, dbname=DB_NAME, port=DB_PORT)
        cursor = conn.cursor()
        
        print(" Initializing High-Performance Traffic Analytics Table...")
        
        # Create a table to track API metrics and response performance
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_logs (
                id SERIAL PRIMARY KEY,
                client_id INT REFERENCES b2b_clients(id) ON DELETE CASCADE,
                endpoint VARCHAR(255) NOT NULL,
                response_time_ms INT NOT NULL,
                status_code INT NOT NULL,
                accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        
        conn.commit()
        print(" Analytics tracking architecture successfully mounted in PostgreSQL!")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f" Metrics Setup Failed: {e}")

if __name__ == "__main__":
    create_metrics_table()