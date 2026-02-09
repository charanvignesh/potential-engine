import pandas as pd
import numpy as np
import os

# ---------------------------
#  SETTINGS
# ---------------------------

save_path = r"E:\VII th SEMESTER\PROJECT\MOTOR_DATA"

os.makedirs(save_path, exist_ok=True)

rows = 1200  # 5 hours @ 15 sec window

# -----------------------------------------
#  RANGE DEFINITIONS (REALISTIC SYNTHETIC DATA)
# -----------------------------------------

def generate_data(condition):

    if condition == "No_load_condition":
        vib_range = (0.5, 1.5)     # mm/s
        mag_range = (2, 5)         # mT

    elif condition == "Front_bearing_damage":
        vib_range = (2.5, 4.5)     # more vibration on X (front)
        mag_range = (6, 12)        # higher magnetic noise

    elif condition == "Back_bearing_damage":
        vib_range = (2.5, 4.5)     # more vibration on Z (rear)
        mag_range = (6, 11)

    elif condition == "Uneven_load_condition":
        vib_range = (4, 7)         # large vibration due to imbalance
        mag_range = (3, 6)         # minor magnetic disturbance

    else:
        raise ValueError("Invalid condition")

    # Generate synthetic vibration data
    vib_x = np.random.uniform(vib_range[0], vib_range[1], rows)
    vib_y = np.random.uniform(vib_range[0], vib_range[1], rows)
    vib_z = np.random.uniform(vib_range[0], vib_range[1], rows)

    # Generate synthetic MLX90393 magnetometer data
    mag_x = np.random.uniform(mag_range[0], mag_range[1], rows)
    mag_y = np.random.uniform(mag_range[0], mag_range[1], rows)
    mag_z = np.random.uniform(mag_range[0], mag_range[1], rows)

    df = pd.DataFrame({
        "Condition": [condition] * rows,
        "Vibration X (mm/s)": vib_x,
        "Vibration Y (mm/s)": vib_y,
        "Vibration Z (mm/s)": vib_z,
        "MLX90393 X (mT)": mag_x,
        "MLX90393 Y (mT)": mag_y,
        "MLX90393 Z (mT)": mag_z,
    })

    return df


# ---------------------------
#  CREATE AND SAVE ALL FILES
# ---------------------------

conditions = {
    "No_load_condition": "No_load_condition.xlsx",
    "Front_bearing_damage": "Front_bearing_damage.xlsx",
    "Back_bearing_damage": "Back_bearing_damage.xlsx",
    "Uneven_load_condition": "Uneven_load_condition.xlsx"
}

for cond, filename in conditions.items():
    df = generate_data(cond)
    df.to_excel(os.path.join(save_path, filename), index=False)

print("✅ All 4 condition sheets generated successfully!")
