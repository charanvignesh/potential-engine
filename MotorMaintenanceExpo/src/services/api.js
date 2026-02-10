import axios from 'axios';
import { API_BASE_URL } from '../utils/constants';

/**
 * Upload motor data and get prediction
 * @param {Object} motorDetails - Motor specifications
 * @param {Object} csvFile - File asset from expo-document-picker
 * @returns {Promise<Object>} - Prediction results
 */
export const analyzeMotor = async (motorDetails, csvFile) => {
    try {
        const formData = new FormData();

        // Add motor details
        formData.append('motor_type', motorDetails.motorType);
        formData.append('phase_type', motorDetails.phaseType);
        formData.append('hp', motorDetails.hp);
        formData.append('voltage', motorDetails.voltage);

        // Add CSV file (Expo Document Picker format)
        const fileToUpload = {
            uri: csvFile.uri,
            type: csvFile.mimeType || 'text/csv',
            name: csvFile.name || 'data.csv',
        };

        formData.append('file', fileToUpload);

        console.log('Sending request to:', `${API_BASE_URL}/api/predict`);

        const response = await axios.post(`${API_BASE_URL}/api/predict`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
            timeout: 30000, // 30 second timeout
        });

        return response.data;
    } catch (error) {
        console.error('API Error:', error);
        if (error.response) {
            // Server responded with error
            throw new Error(error.response.data.error || 'Server error occurred');
        } else if (error.request) {
            // No response received
            throw new Error('Cannot connect to server. Please check if the Flask app is running and your device is on the same network.');
        } else {
            // Other errors
            throw new Error(error.message || 'An unexpected error occurred');
        }
    }
};

/**
 * Get prediction from ThingSpeak data
 * @param {string} channelId - ThingSpeak Channel ID
 * @param {string} apiKey - Read API Key (optional)
 * @returns {Promise<Object>} - Prediction results
 */
export const analyzeMotorThingSpeak = async (channelId, apiKey) => {
    try {
        console.log('Sending ThingSpeak request to:', `${API_BASE_URL}/api/predict_thingspeak`);

        const response = await axios.post(`${API_BASE_URL}/api/predict_thingspeak`, {
            channel_id: channelId,
            api_key: apiKey
        }, {
            timeout: 30000,
        });

        return response.data;
    } catch (error) {
        console.error('API Error:', error);
        if (error.response) {
            throw new Error(error.response.data.error || 'Server error occurred');
        } else if (error.request) {
            throw new Error('Cannot connect to server. Please check if the Flask app is running.');
        } else {
            throw new Error(error.message || 'An unexpected error occurred');
        }
    }
};
