// API Configuration
// For Android Emulator: use 'http://10.0.2.2:5000'
// For Real Device: use your computer's IP address (e.g., http://192.168.1.x:5000)
export const API_BASE_URL = 'https://potential-engine-4.onrender.com';

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
