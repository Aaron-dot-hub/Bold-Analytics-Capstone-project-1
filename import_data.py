import os
import glob
import pandas as pd
import psycopg2

# Database connection details
DB_HOST = "localhost"
DB_USER = "postgres"
DB_PASS = "@A5+m14-E1*n13/"  #  Change this to your real PostgreSQL password!
DB_PORT = "5432"
DB_NAME = "capstone_locations"

def get_db_connection():
    return psycopg2.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, port=DB_PORT, dbname=DB_NAME)

def ingest_all_data():
    # Gather both .xls and .ods files
    data_folder = "./data"
    files = glob.glob(os.path.join(data_folder, "*.xls")) + glob.glob(os.path.join(data_folder, "*.ods"))
    
    if not files:
        print(" No location files discovered in the data folder.")
        return

    print(f" Found {len(files)} state files. Beginning high-volume processing...")
    
    conn = get_db_connection()
    cursor = conn.cursor()

    for file_path in files:
        file_name = os.path.basename(file_path)
        print(f"\n⚡ Processing state file: {file_name}")
        
        try:
            # Determine engine based on extension
            engine = "odf" if file_name.endswith(".ods") else "xlrd"
            df = pd.read_excel(file_path, engine=engine)
            
            # Clean structural spacing from column headers
            df.columns = [str(col).strip() for col in df.columns]
            
            # Row counter for feedback
            rows_inserted = 0
            
            for _, row in df.iterrows():
                # Extract text strings cleanly
                state = str(row.get('STATE NAME', '')).strip().upper()
                district = str(row.get('DISTRICT NAME', '')).strip().upper()
                sub_district = str(row.get('SUB-DISTRICT NAME', '')).strip().upper()
                village = str(row.get('Area Name', '')).strip().upper()
                
                #  FILTER: Skip Census summary rows
                if village == state or village == district or village == sub_district:
                    continue
                
                # 1. State Insertion
                cursor.execute(
                    "INSERT INTO states (state_name) VALUES (%s) ON CONFLICT (state_name) DO UPDATE SET state_name=EXCLUDED.state_name RETURNING id;", 
                    (state,)
                )
                state_id = cursor.fetchone()[0]
                
                # 2. District Insertion (Fixed: using 'district' variable consistently)
                cursor.execute(
                    "INSERT INTO districts (state_id, district_name) VALUES (%s, %s) ON CONFLICT (state_id, district_name) DO UPDATE SET district_name=EXCLUDED.district_name RETURNING id;",
                    (state_id, district)
                )
                district_id = cursor.fetchone()[0]
                
                # 3. Sub-district Insertion
                cursor.execute(
                    "INSERT INTO sub_districts (district_id, sub_district_name) VALUES (%s, %s) ON CONFLICT (district_id, sub_district_name) DO UPDATE SET sub_district_name=EXCLUDED.sub_district_name RETURNING id;",
                    (district_id, sub_district)
                )
                sub_district_id = cursor.fetchone()[0]
                
                # 4. Village Insertion
                cursor.execute(
                    "INSERT INTO villages (sub_district_id, village_name, pincode) VALUES (%s, %s, NULL);",
                    (sub_district_id, village)
                )
                
                rows_inserted += 1
            
            # Commit after every state file completes to secure your data chunks
            conn.commit()
            print(f" Ingested {rows_inserted} clean village records from {file_name}")
            
        except Exception as e:
            conn.rollback()
            print(f" Failed to parse file {file_name} due to error: {e}")

    cursor.close()
    conn.close()
    print("\n All state files have been normalized and pushed into PostgreSQL successfully!")

if __name__ == "__main__":
    ingest_all_data()