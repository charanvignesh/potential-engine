import pandas as pd
import numpy as np
import os

# Parameters
time_window_sec = 15
total_hours = 1
total_rows = int((total_hours * 60 * 60) / time_window_sec)

def generate_data(filename, vib_scale=1.0, mag_scale=1.0):
    print(f"Generating {filename} with vib_scale={vib_scale}, mag_scale={mag_scale}")
    
    # Vibration ranges (mm/s)
    # Normal is approx rms 1.0 (so range -1.7 to 1.7 or 0 to 2?)
    # Training data had 0-2 range for vib presumably? 
    # Centroid Vib RMS is ~0.97. 
    # Uniform(0, 2) has RMS ~1.15. So 0-2 is "Normal-ish".
    vibration_x = np.random.uniform(0.0, 2.0 * vib_scale, total_rows)
    vibration_y = np.random.uniform(0.0, 2.0 * vib_scale, total_rows)
    vibration_z = np.random.uniform(0.0, 2.0 * vib_scale, total_rows)

    # MLX90393 ranges (mT)
    # Centroid Mag RMS is ~3.5.
    # Uniform(-a, a) has RMS = a / sqrt(3).
    # 3.5 = a / 1.732 => a = 3.5 * 1.732 = 6.06.
    # So Normal range height be approx -6 to 6.
    mag_limit = 6.0 * mag_scale
    mlx_x = np.random.uniform(-mag_limit, mag_limit, total_rows)
    mlx_y = np.random.uniform(-mag_limit, mag_limit, total_rows)
    mlx_z = np.random.uniform(-mag_limit, mag_limit, total_rows)

    # Create DataFrame
    df = pd.DataFrame({
        "Vibration X (mm/s)": vibration_x,
        "Vibration Y (mm/s)": vibration_y,
        "Vibration Z (mm/s)": vibration_z,
        "MLX90393 X (mT)": mlx_x,
        "MLX90393 Y (mT)": mlx_y,
        "MLX90393 Z (mT)": mlx_z
    })

    # Save path
    save_path = r"c:\Users\chara\OneDrive\Desktop\project\project_ZIP\project\PROJECT_III\CODES_FOR_PROJECT\uploads"
    os.makedirs(save_path, exist_ok=True)
    
    # Save as CSV (app.py reads CSV)
    # Check if filename ends with csv
    if not filename.endswith(".csv"):
        filename += ".csv"
        
    df.to_csv(os.path.join(save_path, filename), index=False)
    print(f"Saved to {os.path.join(save_path, filename)}")

# Generate 3 datasets
# 1. Normal-ish (matches centroid roughly)
generate_data("Test_Data_Normal.csv", vib_scale=1.0, mag_scale=1.0)

# 2. Moderate Fault (Higher deviation)
# Vib range 0-4 (RMS ~2.3), Mag range -12 to 12 (RMS ~7)
generate_data("Test_Data_Warning.csv", vib_scale=2.0, mag_scale=2.0)

# 3. Critical Fault (Very high deviation)
# Vib range 0-10 (RMS ~5.7), Mag range -30 to 30 (RMS ~17)
generate_data("Test_Data_Critical.csv", vib_scale=5.0, mag_scale=5.0)
