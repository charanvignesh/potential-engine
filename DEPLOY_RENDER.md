# ☁️ How to Deploy Backend to Render

To make your app work anywhere (not just on your home WiFi), you need to host the Python backend on the cloud. We will use **Render** because it's free and easy.

## 📋 Prerequisites
1.  **GitHub Account**: You need to host your code on GitHub first.
2.  **Render Account**: Sign up at [render.com](https://render.com).

## 🚀 Step 1: Push Code to GitHub
You need to create a repository on GitHub and upload your code.

1.  Initialize Git (if not already done):
    ```powershell
    git init
    git add .
    git commit -m "Initial commit"
    ```
2.  Create a new repository on GitHub.
3.  Push your code to the new repository.

## 🚀 Step 2: Deploy on Render
1.  Log in to [dashboard.render.com](https://dashboard.render.com/).
2.  Click **"New +"** and select **"Web Service"**.
3.  Connect your GitHub account and select your repository.
4.  **Configure the Service**:
    *   **Name**: `motor-maintenance-api` (or similar)
    *   **Region**: Closest to you (e.g., Singapore, Frankfurt)
    *   **Branch**: `main` (or master)
    *   **Root Directory**: Leave blank (default)
    *   **Runtime**: **Python 3**
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `gunicorn app:app`
    *   **Instance Type**: **Free**
5.  Click **"Create Web Service"**.

Render will now build your app. Wait for it to show "Live" with a green checkmark.

## 🚀 Step 3: Update Mobile App
Once deployed, Render will give you a URL (e.g., `https://motor-maintenance-api.onrender.com`).

1.  Copy that URL.
2.  Open `MotorMaintenanceExpo/src/utils/constants.js`.
3.  Update the API URL:
    ```javascript
    export const API_BASE_URL = 'https://motor-maintenance-api.onrender.com'; // Your Render URL
    ```
4.  **Rebuild the APK** using EAS:
    ```powershell
    npx eas-cli build -p android --profile preview
    ```

Now your app will work anywhere in the world! 🌍
