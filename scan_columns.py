import os
import glob
import pandas as pd

def scan_files():
    current_dir = os.getcwd()
    print(f" Current Working Directory: {current_dir}")
    
    data_folder = os.path.join(current_dir, "data")
    print(f" Looking for data folder at: {data_folder}")
    print(f" Does folder exist? {os.path.exists(data_folder)}")
    
    # Check what files are directly in the current root folder vs the data folder
    root_files = os.listdir(current_dir)
    print(f" Files in root folder: {root_files}")
    
    if os.path.exists(data_folder):
        data_files = os.listdir(data_folder)
        print(f" Files inside data folder: {data_files}")
    
    # Try searching for files
    files = glob.glob("./data/*.xl*") + glob.glob("./*.xl*")
    
    if not files:
        print("\n No Excel files found (.xls or .xlsx) in root or data folders.")
        return

    first_file = files[0]
    print(f"\n Found a file! Scanning blueprint for: {os.path.basename(first_file)}")
    try:
        df = pd.read_excel(first_file, nrows=5)
        print("\n Exact Column Headers Found:")
        for idx, col in enumerate(df.columns):
            print(f"  {idx + 1}. {col}")
            
        print("\n Sample Record Data:")
        print(df.head(2).to_string(index=False))
        
    except Exception as e:
        print(f" Error reading file: {e}")

if __name__ == "__main__":
    scan_files()