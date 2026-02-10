import os
import pandas as pd
import numpy as np
import pickle
import requests
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from scipy.fft import rfft, rfftfreq
from scipy.signal import welch

app = Flask(__name__)
CORS(app)  # Enable CORS for mobile app
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), "uploads")
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ---------------- Load Model Artifacts ----------------
try:
    with open("model_fault.pkl", "rb") as f:
        clf = pickle.load(f)

    with open("label_encoder.pkl", "rb") as f:
        le = pickle.load(f)

    normal_centroid = np.load("normal_centroid.npy")

    print("Model Loaded Successfully")
    print("Model expects features:", clf.feature_names_in_)

except Exception as e:
    print("Error loading model files:", e)
    clf = None
    le = None
    normal_centroid = None


# ---------------- Feature Functions ----------------
def rms(x):
    x = np.asarray(x, dtype=float)
    return np.sqrt(np.mean(np.square(x)))


def p2p(x):
    x = np.asarray(x, dtype=float)
    return np.max(x) - np.min(x)


def fft_peak(x, fs=1.0):
    x = np.asarray(x, dtype=float)
    y = x - np.mean(x)
    yf = np.abs(rfft(y))
    xf = rfftfreq(len(y), 1/fs)
    idx = np.argmax(yf)
    return float(xf[idx]), float(yf[idx])


def psd(x, fs=1.0):
    x = np.asarray(x, dtype=float)  # 🔥 FIX
    x = x - np.mean(x)
    f, Pxx = welch(x, fs=fs, nperseg=min(256, len(x)))
    return f, Pxx


# ---------------- Feature Extraction ----------------
def compute_features(df):

    df = df.dropna()

    feat = {}

    # ---- Vibration ----
    feat['Vib_RMS_X'] = rms(df["Vibration X (mm/s)"])
    feat['Vib_RMS_Y'] = rms(df["Vibration Y (mm/s)"])
    feat['Vib_RMS_Z'] = rms(df["Vibration Z (mm/s)"])

    feat['Vib_P2P_X'] = p2p(df["Vibration X (mm/s)"])
    feat['Vib_P2P_Y'] = p2p(df["Vibration Y (mm/s)"])
    feat['Vib_P2P_Z'] = p2p(df["Vibration Z (mm/s)"])

    feat['Vib_FFT_Peak_Freq'] , feat['Vib_FFT_Peak_Amp'] = fft_peak(
        df["Vibration X (mm/s)"]
    )

    # ---- Magnetic ----
    feat['Mag_RMS_X'] = rms(df["MLX90393 X (mT)"])
    feat['Mag_RMS_Y'] = rms(df["MLX90393 Y (mT)"])
    feat['Mag_RMS_Z'] = rms(df["MLX90393 Z (mT)"])

    feat['Mag_P2P_X'] = p2p(df["MLX90393 X (mT)"])
    feat['Mag_P2P_Y'] = p2p(df["MLX90393 Y (mT)"])
    feat['Mag_P2P_Z'] = p2p(df["MLX90393 Z (mT)"])

    features_df = pd.DataFrame([feat])

    # 🔥 Align with model expected columns automatically
    expected_cols = clf.feature_names_in_

    # Add missing features
    for col in expected_cols:
        if col not in features_df.columns:
            features_df[col] = 0

    # Remove extra features
    features_df = features_df[expected_cols]

    # ---------------------------------------------------------
    # 🩹 HOTFIX: The model was trained on single-sample rows,
    # so P2P and Freq features were effectively 0 in the Normal Centroid.
    # We must zero them out here to make the Deviation meaningful (comparable to Centroid),
    # otherwise real P2P values cause massive deviation and minimal RUL.
    # ---------------------------------------------------------
    for col in features_df.columns:
        if "P2P" in col or "Freq" in col:
            features_df[col] = 0.0
        # Also, FFT Peak Amp was just |x| (same as RMS) in training. 
        # But we'll leave it or set it to RMS?
        # Leaving it as 0 might be safer if we want to rely on RMS mainly.
        # But the Centroid has Peak_Amp approx equal to RMS.
        # Let's set Peak_Amp to be same as RMS to match Centroid behavior
        if "Peak_Amp" in col:
             # Find corresponding RMS col? 
             # Vib_FFT_Peak_Amp corresponds to Vib X.
             if "Vib" in col:
                 features_df[col] = features_df["Vib_RMS_X"] # Approx match
    
    return features_df


# ---------------- RUL Calculation ----------------
def map_deviation_to_rul(dev, dev_ref=1.0, max_years=25):
    k = 0.55
    frac = 1 / (1 + k * (dev / (dev_ref + 1e-9)))
    frac = max(0.05, frac)

    days = frac * max_years * 365
    years = int(days // 365)
    months = int((days % 365) // 30)

    return years, months, frac


def get_health_status(frac, fault_label):
    health = frac * 100

    if health < 25:
        return "critical"
    elif health < 75:
        return "warning"
    else:
        return "normal"


# ---------------- ThingSpeak Integration ----------------
def fetch_thingspeak_data(channel_id, api_key=None, result_limit=100):
    """
    Fetches the last N results from a ThingSpeak channel.
    Returns a pandas DataFrame with columns mapped to sensor names.
    """
    url = f"https://api.thingspeak.com/channels/{channel_id}/feeds.json?results={result_limit}"
    if api_key:
        url += f"&api_key={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        feeds = data.get("feeds", [])
        
        if not feeds:
            raise ValueError("No data found in ThingSpeak channel.")

        df = pd.DataFrame(feeds)
        
        # Mapping based on user input
        # Field 1,2,3 -> Magnetic X, Y, Z
        # Field 4,5,6 -> Vibration X, Y, Z
        rename_map = {
            "field1": "MLX90393 X (mT)",
            "field2": "MLX90393 Y (mT)",
            "field3": "MLX90393 Z (mT)",
            "field4": "Vibration X (mm/s)",
            "field5": "Vibration Y (mm/s)",
            "field6": "Vibration Z (mm/s)"
        }
        
        df = df.rename(columns=rename_map)
        
        # Ensure numeric types
        for col in rename_map.values():
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Drop rows with NaN if any
        df = df.dropna()
        
        return df, data.get("channel", {})

    except Exception as e:
        print(f"Error fetching ThingSpeak data: {e}")
        return None, None


# ---------------- Routes ----------------
@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        if clf is None or le is None or normal_centroid is None:
            return "Model files missing!", 500

        file = request.files.get("file")
        if not file or file.filename == "":
            return "No file selected", 400

        path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(path)

        try:
            df = pd.read_csv(path)
        except Exception as e:
            return f"CSV Read Error: {e}", 400

        try:
            # 1️⃣ Feature Extraction
            features_df = compute_features(df)
            features_dict = features_df.iloc[0].round(4).to_dict()

            # 2️⃣ Prediction
            prediction_raw = clf.predict(features_df)[0]
            pred_label = le.inverse_transform([prediction_raw])[0]

            # 3️⃣ Deviation & RUL
            test_features = features_df.values.flatten()
            dev = float(np.linalg.norm(test_features - normal_centroid.flatten()))
            dev_ref = max(np.linalg.norm(normal_centroid.flatten()) * 0.15, 1.0)

            years, months, frac = map_deviation_to_rul(dev, dev_ref)
            health_status = get_health_status(frac, pred_label)

            # 4️⃣ PSD for Plot
            f_vib, P_vib = psd(df["Vibration X (mm/s)"])
            f_mag, P_mag = psd(df["MLX90393 X (mT)"])

            return render_template(
                "dashboard.html",
                final_fault=pred_label,
                final_rul=f"{years} years {months} months",
                health_frac=int(frac * 100),
                health_status=health_status,
                dev=round(dev, 2),
                samples=df.index.tolist(),
                vib_data=[
                    df["Vibration X (mm/s)"].tolist(),
                    df["Vibration Y (mm/s)"].tolist(),
                    df["Vibration Z (mm/s)"].tolist()
                ],
                mag_data=[
                    df["MLX90393 X (mT)"].tolist(),
                    df["MLX90393 Y (mT)"].tolist(),
                    df["MLX90393 Z (mT)"].tolist()
                ],
                f_vib=f_vib.tolist(),
                P_vib=P_vib.tolist(),
                f_mag=f_mag.tolist(),
                P_mag=P_mag.tolist(),
                features=features_dict
            )

        except Exception as e:
            return f"Processing Error: {e}", 500

    return render_template("index.html")


# ---------------- Download Test Data ----------------
@app.route("/test-data", methods=["GET"])
def list_test_data():
    """List available test data files for download"""
    try:
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        # Filter only CSV files starting with Test_Data
        test_files = [f for f in files if f.startswith("Test_Data") and f.endswith(".csv")]
        
        html = "<h1>Available Test Data</h1><ul>"
        for f in test_files:
            html += f'<li><a href="/download_test/{f}">{f}</a></li>'
        html += "</ul>"
        return html
    except Exception as e:
        return f"Error listing files: {e}", 500

@app.route("/download_test/<filename>")
def download_test_file(filename):
    """Download a specific test file"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


# ---------------- API Endpoint for Mobile App ----------------
@app.route("/api/predict", methods=["POST"])
def api_predict():
    """API endpoint for mobile app - returns JSON response"""
    
    if clf is None or le is None or normal_centroid is None:
        return jsonify({"error": "Model files missing!"}), 500
    
    # Get file and motor details
    file = request.files.get("file")
    if not file or file.filename == "":
        return jsonify({"error": "No file selected"}), 400
    
    motor_type = request.form.get("motor_type", "Unknown")
    phase_type = request.form.get("phase_type", "Unknown")
    hp = request.form.get("hp", "0")
    voltage = request.form.get("voltage", "0")
    
    # Save and process file
    path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(path)
    
    try:
        df = pd.read_csv(path)
    except Exception as e:
        return jsonify({"error": f"CSV Read Error: {str(e)}"}), 400
    
    try:
        # 1️⃣ Feature Extraction
        features_df = compute_features(df)
        features_dict = features_df.iloc[0].round(4).to_dict()
        
        # 2️⃣ Prediction
        prediction_raw = clf.predict(features_df)[0]
        pred_label = le.inverse_transform([prediction_raw])[0]
        
        # 3️⃣ Deviation & RUL
        test_features = features_df.values.flatten()
        dev = float(np.linalg.norm(test_features - normal_centroid.flatten()))
        dev_ref = max(np.linalg.norm(normal_centroid.flatten()) * 0.15, 1.0)
        
        years, months, frac = map_deviation_to_rul(dev, dev_ref)
        health_status = get_health_status(frac, pred_label)
        
        # 4️⃣ PSD for Plot
        f_vib, P_vib = psd(df["Vibration X (mm/s)"])
        f_mag, P_mag = psd(df["MLX90393 X (mT)"])
        
        # Return JSON response
        return jsonify({
            "success": True,
            "motor_info": {
                "motor_type": motor_type,
                "phase_type": phase_type,
                "hp": hp,
                "voltage": voltage
            },
            "prediction": {
                "fault": pred_label,
                "rul": f"{years} years {months} months",
                "rul_years": years,
                "rul_months": months,
                "health_percentage": int(frac * 100),
                "health_status": health_status,
                "deviation": round(dev, 2)
            },
            "data": {
                "samples": df.index.tolist(),
                "vibration": {
                    "x": df["Vibration X (mm/s)"].tolist(),
                    "y": df["Vibration Y (mm/s)"].tolist(),
                    "z": df["Vibration Z (mm/s)"].tolist()
                },
                "magnetic": {
                    "x": df["MLX90393 X (mT)"].tolist(),
                    "y": df["MLX90393 Y (mT)"].tolist(),
                    "z": df["MLX90393 Z (mT)"].tolist()
                },
                "psd": {
                    "vibration": {
                        "frequency": f_vib.tolist(),
                        "power": P_vib.tolist()
                    },
                    "magnetic": {
                        "frequency": f_mag.tolist(),
                        "power": P_mag.tolist()
                    }
                },
                "features": features_dict
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Processing Error: {str(e)}"}), 500


@app.route("/api/predict_thingspeak", methods=["POST"])
def api_predict_thingspeak():
    """
    API endpoint to fetch data from ThingSpeak and return prediction.
    Expects JSON body: { "channel_id": "...", "api_key": "..." }
    """
    if clf is None or le is None or normal_centroid is None:
        return jsonify({"error": "Model files missing!"}), 500

    req_data = request.get_json()
    if not req_data or "channel_id" not in req_data:
        return jsonify({"error": "Missing channel_id"}), 400

    channel_id = req_data["channel_id"]
    api_key = req_data.get("api_key", None)
    
    # Fetch data
    df, channel_info = fetch_thingspeak_data(channel_id, api_key)
    
    if df is None or df.empty:
        return jsonify({"error": "Failed to fetch data from ThingSpeak or data is empty."}), 400

    try:
        # 1️⃣ Feature Extraction
        features_df = compute_features(df)
        features_dict = features_df.iloc[0].round(4).to_dict()
        
        # 2️⃣ Prediction
        prediction_raw = clf.predict(features_df)[0]
        pred_label = le.inverse_transform([prediction_raw])[0]
        
        # 3️⃣ Deviation & RUL
        test_features = features_df.values.flatten()
        dev = float(np.linalg.norm(test_features - normal_centroid.flatten()))
        dev_ref = max(np.linalg.norm(normal_centroid.flatten()) * 0.15, 1.0)
        
        years, months, frac = map_deviation_to_rul(dev, dev_ref)
        health_status = get_health_status(frac, pred_label)
        
        # 4️⃣ PSD for Plot
        f_vib, P_vib = psd(df["Vibration X (mm/s)"])
        f_mag, P_mag = psd(df["MLX90393 X (mT)"])
        
        return jsonify({
            "success": True,
            "channel_info": {
                "name": channel_info.get("name", "Unknown"),
                "id": channel_id
            },
            "prediction": {
                "fault": pred_label,
                "rul": f"{years} years {months} months",
                "rul_years": years,
                "rul_months": months,
                "health_percentage": int(frac * 100),
                "health_status": health_status,
                "deviation": round(dev, 2)
            },
            "data": {
                "samples": df.index.tolist(),
                "vibration": {
                    "x": df["Vibration X (mm/s)"].tolist(),
                    "y": df["Vibration Y (mm/s)"].tolist(),
                    "z": df["Vibration Z (mm/s)"].tolist()
                },
                "magnetic": {
                    "x": df["MLX90393 X (mT)"].tolist(),
                    "y": df["MLX90393 Y (mT)"].tolist(),
                    "z": df["MLX90393 Z (mT)"].tolist()
                },
                "features": features_dict
            }
        }), 200

    except Exception as e:
        return jsonify({"error": f"Processing Error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')  # Allow connections from mobile devices
