import pandas as pd
import numpy as np
import glob
import os

# Path where your Excel files are stored
folder = r"E:\VII th SEMESTER\PROJECT\MOTOR_DATA"

# Read all .xlsx files
files = glob.glob(os.path.join(folder, "*.xlsx"))

all_data = []

for f in files:
    df = pd.read_excel(f)
    
    # Clean column names (remove spaces)
    df.columns = [
        c.strip().replace(" ", "_").replace("(", "").replace(")", "") 
        for c in df.columns
    ]
    
    # Add filename as sample source
    df["source_file"] = os.path.basename(f)
    
    all_data.append(df)

# Combine everything
combined = pd.concat(all_data, ignore_index=True)

# Save as CSV
combined.to_csv(os.path.join(folder, "combined_dataset.csv"), index=False)

print("combined_dataset.csv created successfully!")
