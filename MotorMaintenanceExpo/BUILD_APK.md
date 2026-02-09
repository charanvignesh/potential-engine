# 🏗️ How to Build a Standalone APK

If you want to install the app on your phone without using the "Expo Go" app, you can build a standalone **APK file**.

## 📋 Prerequisites

1.  **Expo Account**: You need a free account at [expo.dev](https://expo.dev/signup).
2.  **EAS CLI**: We've already installed the build tools for you.

## 🚀 Build Instructions

1.  **Open Terminal** in the `MotorMaintenanceExpo` folder.

2.  **Run the Build Command**:
    ```powershell
    npx --package eas-cli eas build -p android --profile preview
    ```

3.  **Follow the Prompts**:
    *   **Log in**: Enter your Expo email and password when asked.
    *   **Generate Keystore**: Select **"Yes"** (Y) to let Expo manage your credentials automatically.
    *   **Package Name**: Accept the default or type a unique name (e.g., `com.yourname.motormaintenance`).

4.  **Wait for Build**:
    *   The build runs in the cloud and takes about **10-15 minutes**.
    *   You can close the terminal if you want; the build continues online.

5.  **Download & Install**:
    *   Once finished, you'll get a **Download Link** (or QR code) in the terminal.
    *   Open that link on your Android phone to download the `.apk` file.
    *   Tap the file to install it (you may need to allow "Install from Unknown Sources").

---

## ⚠️ Important Note about API URL

Since the standalone app runs on your real phone, ensure your `src/utils/constants.js` is configured with your computer's **current IP address**:

```javascript
// Make sure this matches your computer's IP!
export const API_BASE_URL = 'http://192.168.1.5:5000';
```

If your IP changes, you'll need to update this file and rebuild the app (or at least republish the update if using EAS Update).
