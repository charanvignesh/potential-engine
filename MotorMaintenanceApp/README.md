# Motor Maintenance Mobile App

A React Native mobile application for motor predictive maintenance that integrates with a Flask backend to analyze vibration and magnetic sensor data, predict motor faults, and estimate Remaining Useful Life (RUL).

## Features

- 📱 Cross-platform (Android & iOS)
- 📊 Real-time motor health analysis
- 📈 Interactive charts for vibration and magnetic data
- 🎯 Fault prediction using machine learning
- ⏳ RUL (Remaining Useful Life) estimation
- 💚 Visual health score gauge
- 🌙 Modern dark theme UI

## Prerequisites

Before you begin, ensure you have the following installed:

### Required Software

1. **Node.js** (v18 or higher)
   - Download from: https://nodejs.org/
   - Verify installation: `node --version`

2. **npm** or **yarn**
   - Comes with Node.js
   - Verify: `npm --version`

3. **React Native CLI**
   ```bash
   npm install -g react-native-cli
   ```

4. **For Android Development:**
   - Android Studio
   - Android SDK (API level 33 or higher)
   - Java Development Kit (JDK 17)

5. **For iOS Development (macOS only):**
   - Xcode (latest version)
   - CocoaPods: `sudo gem install cocoapods`

## Installation

### 1. Install Dependencies

Navigate to the app directory and install packages:

```bash
cd MotorMaintenanceApp
npm install
```

Or with yarn:
```bash
yarn install
```

### 2. Install Additional Dependencies

Some packages require additional setup:

```bash
# Install Picker component
npm install @react-native-picker/picker

# Link native dependencies (if using React Native < 0.60)
npx react-native link
```

### 3. iOS Setup (macOS only)

```bash
cd ios
pod install
cd ..
```

## Backend Setup

### 1. Start the Flask Backend

The mobile app requires the Flask backend to be running. Navigate to your Flask app directory:

```bash
cd ../CODES_FOR_PROJECT
python app.py
```

The server will start on `http://0.0.0.0:5000`

### 2. Configure API URL

Update the API URL in `src/utils/constants.js` based on your setup:

- **Android Emulator**: Use `http://10.0.2.2:5000` (already configured)
- **iOS Simulator**: Use `http://localhost:5000`
- **Real Device**: Use your computer's local IP address (e.g., `http://192.168.1.100:5000`)

To find your local IP:
- **Windows**: `ipconfig` (look for IPv4 Address)
- **macOS/Linux**: `ifconfig` or `ip addr`

## Running the App

### Android

1. Start an Android emulator or connect a physical device
2. Run the app:
   ```bash
   npx react-native run-android
   ```

### iOS (macOS only)

1. Start an iOS simulator or connect a physical device
2. Run the app:
   ```bash
   npx react-native run-ios
   ```

## Usage

### 1. Upload Motor Data

- Select motor type (AC Induction, DC Brushless, etc.)
- Choose phase type (3-Phase or Single-Phase)
- Enter horsepower (HP)
- Select voltage (240V, 480V, or 600V)
- Upload CSV file with sensor data

### 2. View Analysis Results

The dashboard displays:
- **Motor Information**: Type, phase, HP, voltage
- **Predicted Fault**: Type of fault detected
- **RUL**: Remaining useful life in years and months
- **Health Score**: Visual gauge showing motor health (0-100%)
- **Vibration Charts**: Time series data for vibration sensors
- **Magnetic Charts**: Time series data for magnetic sensors

## CSV File Format

The CSV file should contain the following columns:

```
Vibration X (mm/s), Vibration Y (mm/s), Vibration Z (mm/s), MLX90393 X (mT), MLX90393 Y (mT), MLX90393 Z (mT)
```

Example:
```csv
Vibration X (mm/s),Vibration Y (mm/s),Vibration Z (mm/s),MLX90393 X (mT),MLX90393 Y (mT),MLX90393 Z (mT)
0.12,0.15,0.10,0.05,0.03,0.02
0.13,0.14,0.11,0.06,0.04,0.03
...
```

## Troubleshooting

### Cannot Connect to Server

1. Ensure Flask backend is running
2. Check that your device/emulator can reach the server
3. Verify the API URL in `src/utils/constants.js`
4. For real devices, ensure both device and computer are on the same network

### Build Errors

```bash
# Clean and rebuild
cd android
./gradlew clean
cd ..
npx react-native run-android
```

For iOS:
```bash
cd ios
pod deintegrate
pod install
cd ..
npx react-native run-ios
```

### Metro Bundler Issues

```bash
# Reset Metro cache
npx react-native start --reset-cache
```

## Project Structure

```
MotorMaintenanceApp/
├── src/
│   ├── screens/
│   │   ├── HomeScreen.js          # Upload form
│   │   └── DashboardScreen.js     # Results display
│   ├── services/
│   │   └── api.js                 # Backend API integration
│   ├── styles/
│   │   └── theme.js               # App theme
│   └── utils/
│       └── constants.js           # Configuration
├── App.js                         # Root component
├── index.js                       # Entry point
└── package.json                   # Dependencies
```

## Technologies Used

- **React Native** - Mobile framework
- **React Navigation** - Navigation library
- **Axios** - HTTP client
- **React Native Chart Kit** - Data visualization
- **React Native Circular Progress** - Health gauge
- **React Native Paper** - UI components
- **React Native Document Picker** - File selection

## API Endpoint

The app communicates with the Flask backend via:

**POST** `/api/predict`

**Request:**
- `motor_type`: String
- `phase_type`: String
- `hp`: Number
- `voltage`: Number
- `file`: CSV file (multipart/form-data)

**Response:**
```json
{
  "success": true,
  "motor_info": { ... },
  "prediction": {
    "fault": "Normal",
    "rul": "20 years 5 months",
    "health_percentage": 85,
    "health_status": "normal"
  },
  "data": {
    "vibration": { "x": [...], "y": [...], "z": [...] },
    "magnetic": { "x": [...], "y": [...], "z": [...] }
  }
}
```

## License

This project is part of the Motor Predictive Maintenance system.

## Support

For issues or questions, please check:
1. Flask backend is running on the correct port
2. API URL is configured correctly
3. CSV file format matches requirements
4. Device/emulator has network connectivity
