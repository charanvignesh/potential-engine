import pandas as pd
import numpy as np
from scipy.fft import rfft, rfftfreq

# ----------- Helper Functions --------------

def rms(x):
    return np.sqrt(np.mean(x**2))

def peak_to_peak(x):
    return np.max(x) - np.min(x)

def fft_peak(x, fs=100):
    # fs = 100 Hz assumed sampling rate
    N = len(x)
    yf = np.abs(rfft(x))
    xf = rfftfreq(N, 1/fs)
    peak_freq = xf[np.argmax(yf)]
    peak_amp = np.max(yf)
    return peak_freq, peak_amp

# ----------- MAIN FEATURE EXTRACTION --------------

# Load combined raw data
df = pd.read_csv(r"E:\VII th SEMESTER\PROJECT\MOTOR_DATA\combined_dataset.csv")

feature_rows = []

# Group by Condition (each Excel file becomes one class)
for condition, group in df.groupby("Condition"):

    Vx = group["Vibration_X_mm/s"].values
    Vy = group["Vibration_Y_mm/s"].values
    Vz = group["Vibration_Z_mm/s"].values

    Mx = group["MLX90393_X_mT"].values
    My = group["MLX90393_Y_mT"].values
    Mz = group["MLX90393_Z_mT"].values

    # ----- VIBRATION FEATURES -----
    features = {
        "Condition": condition,

        "Vib_RMS_X": rms(Vx),
        "Vib_RMS_Y": rms(Vy),
        "Vib_RMS_Z": rms(Vz),

        "Vib_P2P_X": peak_to_peak(Vx),
        "Vib_P2P_Y": peak_to_peak(Vy),
        "Vib_P2P_Z": peak_to_peak(Vz),
    }

    # FFT Features (X-axis only for simplicity)
    f_freq, f_amp = fft_peak(Vx)
    features["Vib_FFT_Peak_Freq"] = f_freq
    features["Vib_FFT_Peak_Amp"] = f_amp

    # ----- MAGNETIC FEATURES -----
    features["Mag_RMS_X"] = rms(Mx)
    features["Mag_RMS_Y"] = rms(My)
    features["Mag_RMS_Z"] = rms(Mz)

    features["Mag_P2P_X"] = peak_to_peak(Mx)
    features["Mag_P2P_Y"] = peak_to_peak(My)
    features["Mag_P2P_Z"] = peak_to_peak(Mz)

    # Save row
    feature_rows.append(features)

# Convert to DataFrame
features_df = pd.DataFrame(feature_rows)

# Save file
features_df.to_csv(r"E:\VII th SEMESTER\PROJECT\MOTOR_DATA\features.csv", index=False)

print("features.csv created successfully!")
