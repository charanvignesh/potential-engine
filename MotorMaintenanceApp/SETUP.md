# Quick Setup Guide - Motor Maintenance Mobile App

## 🚀 Quick Start

### Step 1: Install Node.js
1. Download Node.js from https://nodejs.org/ (v18 or higher)
2. Run the installer
3. Verify: Open PowerShell and run `node --version`

### Step 2: Install Dependencies
```powershell
cd MotorMaintenanceApp
npm install
npm install @react-native-picker/picker
```

### Step 3: Start Flask Backend
```powershell
# In a new terminal, navigate to CODES_FOR_PROJECT
cd ..\
python app.py
```

The backend will run on `http://0.0.0.0:5000`

### Step 4: Configure API URL

**For Android Emulator** (default - already configured):
- URL: `http://10.0.2.2:5000`

**For Real Device**:
1. Find your computer's IP address:
   ```powershell
   ipconfig
   ```
   Look for "IPv4 Address" (e.g., 192.168.1.100)

2. Edit `src/utils/constants.js`:
   ```javascript
   export const API_BASE_URL = 'http://YOUR_IP_HERE:5000';
   ```

3. Make sure your phone and computer are on the same WiFi network

### Step 5: Run the App

**Android:**
1. Install Android Studio
2. Open Android Studio → More Actions → Virtual Device Manager
3. Create/Start an emulator
4. In PowerShell:
   ```powershell
   npx react-native run-android
   ```

**iOS (macOS only):**
```bash
cd ios
pod install
cd ..
npx react-native run-ios
```

## 📱 Using the App

1. **Fill Motor Details:**
   - Motor Type: AC Induction, DC Brushless, etc.
   - Phase: 3-Phase or Single-Phase
   - HP: e.g., 7.5
   - Voltage: 240V, 480V, or 600V

2. **Upload CSV File:**
   - Tap "Choose CSV File"
   - Select a CSV with vibration and magnetic sensor data

3. **Analyze:**
   - Tap "Analyze Motor"
   - View results on the dashboard

## 🔧 Troubleshooting

### "Cannot connect to server"
- ✅ Check Flask backend is running
- ✅ Verify API URL in `src/utils/constants.js`
- ✅ For real devices, ensure same WiFi network

### "Module not found"
```powershell
cd MotorMaintenanceApp
npm install
```

### Metro bundler issues
```powershell
npx react-native start --reset-cache
```

## 📂 CSV File Format

Your CSV should have these columns:
```
Vibration X (mm/s), Vibration Y (mm/s), Vibration Z (mm/s), MLX90393 X (mT), MLX90393 Y (mT), MLX90393 Z (mT)
```

## 🎯 What You'll See

- **Motor Info Card**: Your motor specifications
- **Fault Prediction**: Detected fault type
- **RUL**: Remaining useful life (years & months)
- **Health Gauge**: Visual health score (0-100%)
- **Charts**: Vibration and magnetic sensor data visualization

## 📞 Need Help?

Common issues:
1. **npx not recognized**: Install Node.js first
2. **Connection refused**: Start Flask backend
3. **Build failed**: Run `npm install` again
4. **Emulator not starting**: Open Android Studio and start emulator manually

---

For detailed documentation, see [README.md](README.md)
