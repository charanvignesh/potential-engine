# 🚀 Quick Start Guide - Expo Mobile App

This version of the app uses **Expo**, which makes it much easier to run on Android Emulators or real devices without complex setup.

## 📋 Prerequisites

1.  **Node.js**: [Download & Install](https://nodejs.org/) (v18+)
2.  **Android Studio**: For running the Android Emulator

## 🛠️ Setup Instructions

### 1. Start the Backend
Open a terminal in the main project folder (`CODES_FOR_PROJECT`) and run:
```powershell
python app.py
```
*Keep this terminal open!*

### 2. Start Android Emulator
1.  Open **Android Studio**
2.  Go to **More Actions** -> **Virtual Device Manager**
3.  Click the **▶ Play** button next to your virtual device
4.  Wait for the emulator to fully boot up

### 3. Run the Mobile App
Open a **new** terminal, navigate to the Expo project folder, and start the app:

```powershell
cd MotorMaintenanceExpo
npx expo start --android
```

The app will build and automatically launch on your emulator!

---

## 📱 Running on a Real Device (Optional)

If you prefer to use your physical Android phone instead of an emulator:

1.  Download the **Expo Go** app from the Google Play Store on your phone.
2.  Connect your phone and computer to the **same WiFi network**.
3.  Find your computer's IP address:
    ```powershell
    ipconfig
    ```
4.  Update `src/utils/constants.js`:
    ```javascript
    export const API_BASE_URL = 'http://YOUR_COMPUTER_IP:5000';
    ```
5.  Run the app:
    ```powershell
    npx expo start
    ```
6.  Scan the QR code shown in the terminal using the **Expo Go** app.

---

## ❓ Troubleshooting

*   **"Network Request Failed"**: 
    *   Make sure Flask backend is running.
    *   If on Emulator, ensure `API_BASE_URL` is `http://10.0.2.2:5000`.
    *   If on Real Device, ensure `API_BASE_URL` is your computer's IP and both devices are on the same WiFi.

*   **"Expo not found"**:
    *   Run `npm install -g expo-cli`

*   **"Android project not found"**:
    *   Make sure you are in the `MotorMaintenanceExpo` folder, NOT the old `MotorMaintenanceApp` folder.
