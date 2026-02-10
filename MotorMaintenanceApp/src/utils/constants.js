// API Configuration
// For Android Emulator: use 'http://10.0.2.2:5000'
// For iOS Simulator: use 'http://localhost:5000'
// For Real Device: use your computer's IP address
export const API_BASE_URL = 'https://potential-engine-1.onrender.com'; // Updated with your computer's IP

export const MOTOR_TYPES = [
  { label: 'AC Induction', value: 'AC Induction' },
  { label: 'DC Brushless', value: 'DC Brushless' },
  { label: 'Synchronous', value: 'Synchronous' },
  { label: 'Stepper', value: 'Stepper' },
];

export const PHASE_TYPES = [
  { label: '3-Phase', value: '3-Phase' },
  { label: 'Single-Phase', value: 'Single-Phase' },
];

export const VOLTAGES = [
  { label: '240 V', value: '240' },
  { label: '480 V', value: '480' },
  { label: '600 V', value: '600' },
];
