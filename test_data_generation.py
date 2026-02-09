import pandas as pd
import numpy as np
import os

# Parameters
time_window_sec = 15
total_hours = 1
total_rows = int((total_hours * 60 * 60) / time_window_sec)

# Vibration ranges (mm/s) - adjust as needed
vib_ranges = {
    "x": (0.0, 2.0),
    "y": (0.0, 2.0),
    "z": (0.0, 2.0)
}

# MLX90393 ranges (mT) - adjust as needed
mlx_ranges = {
    "x": (-50, 50),
    "y": (-50, 50),
    "z": (-50, 50)
}

# Generate random data
vibration_x = np.random.uniform(vib_ranges["x"][0], vib_ranges["x"][1], total_rows)
vibration_y = np.random.uniform(vib_ranges["y"][0], vib_ranges["y"][1], total_rows)
vibration_z = np.random.uniform(vib_ranges["z"][0], vib_ranges["z"][1], total_rows)

mlx_x = np.random.uniform(mlx_ranges["x"][0], mlx_ranges["x"][1], total_rows)
mlx_y = np.random.uniform(mlx_ranges["y"][0], mlx_ranges["y"][1], total_rows)
mlx_z = np.random.uniform(mlx_ranges["z"][0], mlx_ranges["z"][1], total_rows)

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
save_path = r"E:\VII th SEMESTER\PROJECT\MOTOR_DATA"
os.makedirs(save_path, exist_ok=True)
filename = "Test_data_1hour.xlsx"

df.to_excel(os.path.join(save_path, filename), index=False)

print(f"Test data saved to {os.path.join(save_path, filename)}")
