# =====================================================
# MOTOR CONDITION MONITORING - HYBRID MODEL TRAINING
# =====================================================

import pandas as pd
import numpy as np
import pickle
from scipy.fft import rfft, rfftfreq
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt

# ----------------------------
# STEP 1: LOAD RAW DATA
# ----------------------------
data_path = r"E:\VII th SEMESTER\PROJECT\MOTOR_DATA\combined_dataset.csv"
df = pd.read_csv(data_path)

print("Combined dataset loaded successfully.\n")
print("Columns available:", df.columns.tolist(), "\n")
print("Total samples:", len(df), "\n")

# ----------------------------
# STEP 2: HELPER FUNCTIONS FOR FEATURE EXTRACTION
# ----------------------------
def rms(x):
    return np.sqrt(np.mean(np.array(x)**2))

def peak_to_peak(x):
    return np.max(x) - np.min(x)

def fft_peak(x, fs=1):  # fs can be 1 if relative
    x = np.array(x)
    N = len(x)
    yf = np.abs(rfft(x))
    xf = rfftfreq(N, 1/fs)
    peak_freq = xf[np.argmax(yf)]
    peak_amp = np.max(yf)
    return peak_freq, peak_amp

# ----------------------------
# STEP 3: FEATURE EXTRACTION PER ROW
# ----------------------------
feature_rows = []

for idx, row in df.iterrows():
    features = {}
    features["Condition"] = row["Condition"]
    
    # Vibration features
    Vx, Vy, Vz = row["Vibration_X_mm/s"], row["Vibration_Y_mm/s"], row["Vibration_Z_mm/s"]
    features["Vib_RMS_X"] = rms([Vx])
    features["Vib_RMS_Y"] = rms([Vy])
    features["Vib_RMS_Z"] = rms([Vz])
    features["Vib_P2P_X"] = peak_to_peak([Vx])
    features["Vib_P2P_Y"] = peak_to_peak([Vy])
    features["Vib_P2P_Z"] = peak_to_peak([Vz])
    f_freq, f_amp = fft_peak([Vx])
    features["Vib_FFT_Peak_Freq"] = f_freq
    features["Vib_FFT_Peak_Amp"] = f_amp

    # Magnetic features
    Mx, My, Mz = row["MLX90393_X_mT"], row["MLX90393_Y_mT"], row["MLX90393_Z_mT"]
    features["Mag_RMS_X"] = rms([Mx])
    features["Mag_RMS_Y"] = rms([My])
    features["Mag_RMS_Z"] = rms([Mz])
    features["Mag_P2P_X"] = peak_to_peak([Mx])
    features["Mag_P2P_Y"] = peak_to_peak([My])
    features["Mag_P2P_Z"] = peak_to_peak([Mz])
    
    feature_rows.append(features)

features_df = pd.DataFrame(feature_rows)
print("Feature extraction completed. Total feature rows:", len(features_df), "\n")

# ----------------------------
# STEP 4: PREPARE DATA FOR TRAINING
# ----------------------------
feature_cols = [
    "Vib_RMS_X", "Vib_RMS_Y", "Vib_RMS_Z",
    "Vib_P2P_X", "Vib_P2P_Y", "Vib_P2P_Z",
    "Vib_FFT_Peak_Freq", "Vib_FFT_Peak_Amp",
    "Mag_RMS_X", "Mag_RMS_Y", "Mag_RMS_Z",
    "Mag_P2P_X", "Mag_P2P_Y", "Mag_P2P_Z"
]

X = features_df[feature_cols].copy()
y_fault = features_df["Condition"].copy()
le = LabelEncoder()
y_fault_encoded = le.fit_transform(y_fault)
print("Fault labels encoded.\n")

# Save label encoder
with open("label_encoder.pkl", "wb") as f:
    pickle.dump(le, f)
print("Label encoder saved as label_encoder.pkl\n")

# ----------------------------
# STEP 5: COMPUTE NORMAL FEATURE CENTROID
# ----------------------------
normal_features = features_df[features_df["Condition"] == "No_load_condition"]
normal_centroid = normal_features[feature_cols].mean().values
np.save("normal_centroid.npy", normal_centroid)
print("Normal feature centroid computed and saved as normal_centroid.npy\n")

# ----------------------------
# STEP 6: TRAIN FAULT CLASSIFIER WITH CROSS-VALIDATION
# ----------------------------
clf = RandomForestClassifier(
    n_estimators=250,
    max_depth=None,
    min_samples_split=4,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

n_samples = len(X)
n_splits = 5 if n_samples >= 5 else n_samples
skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)

print(f"Training Fault Classifier using {n_splits}-fold cross-validation...\n")
y_pred_cv = cross_val_predict(clf, X, y_fault_encoded, cv=skf)

# ----------------------------
# STEP 7: EVALUATE FAULT CLASSIFIER
# ----------------------------
accuracy = accuracy_score(y_fault_encoded, y_pred_cv)
print(f"Fault Classification Accuracy (CV): {accuracy*100:.2f}%\n")

print("Confusion Matrix:\n")
print(confusion_matrix(y_fault_encoded, y_pred_cv), "\n")

print("Classification Report:\n")
print(classification_report(y_fault_encoded, y_pred_cv), "\n")

# Train on full dataset
clf.fit(X, y_fault_encoded)
with open("model_fault.pkl", "wb") as f:
    pickle.dump(clf, f)
print("Fault classifier trained on full dataset and saved as model_fault.pkl\n")

# ----------------------------
# STEP 8: FEATURE IMPORTANCE VISUALIZATION
# ----------------------------
feat_importances = pd.Series(clf.feature_importances_, index=X.columns)
plt.figure(figsize=(12,6))
feat_importances.sort_values().plot(kind='barh', color='skyblue')
plt.title("Feature Importance - Fault Classification")
plt.xlabel("Importance")
plt.ylabel("Features")
plt.tight_layout()
plt.show()

print("Hybrid model training pipeline completed successfully.\n")
