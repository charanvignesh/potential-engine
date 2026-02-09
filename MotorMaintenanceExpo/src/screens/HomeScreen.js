import React, { useState } from 'react';
import {
    View,
    Text,
    StyleSheet,
    ScrollView,
    TouchableOpacity,
    Alert,
    ActivityIndicator,
    TextInput,
} from 'react-native';
import { Picker } from '@react-native-picker/picker';
import * as DocumentPicker from 'expo-document-picker';
import { theme } from '../styles/theme';
import { MOTOR_TYPES, PHASE_TYPES, VOLTAGES } from '../utils/constants';
import { analyzeMotor } from '../services/api';

const HomeScreen = ({ navigation }) => {
    const [motorType, setMotorType] = useState('');
    const [phaseType, setPhaseType] = useState('');
    const [hp, setHp] = useState('');
    const [voltage, setVoltage] = useState('');
    const [csvFile, setCsvFile] = useState(null);
    const [loading, setLoading] = useState(false);

    const pickDocument = async () => {
        try {
            const result = await DocumentPicker.getDocumentAsync({
                type: ['text/csv', 'text/comma-separated-values', 'application/csv'],
                copyToCacheDirectory: true,
            });

            if (!result.canceled && result.assets && result.assets.length > 0) {
                const file = result.assets[0];
                setCsvFile(file);
                Alert.alert('Success', `File selected: ${file.name}`);
            }
        } catch (err) {
            Alert.alert('Error', 'Failed to pick file');
            console.error(err);
        }
    };

    const handleAnalyze = async () => {
        // Validation
        if (!motorType || !phaseType || !hp || !voltage) {
            Alert.alert('Error', 'Please fill in all motor details');
            return;
        }
        if (!csvFile) {
            Alert.alert('Error', 'Please select a CSV file');
            return;
        }

        setLoading(true);
        try {
            const motorDetails = {
                motorType,
                phaseType,
                hp,
                voltage,
            };

            const result = await analyzeMotor(motorDetails, csvFile);

            if (result.success) {
                navigation.navigate('Dashboard', { data: result });
            } else {
                Alert.alert('Error', result.error || 'Analysis failed');
            }
        } catch (error) {
            Alert.alert('Error', error.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <ScrollView style={styles.container}>
            <View style={styles.header}>
                <Text style={styles.title}>⚙️ Motor Predictive Maintenance</Text>
                <Text style={styles.subtitle}>
                    Upload operational data to diagnose fault and predict RUL
                </Text>
            </View>

            <View style={styles.card}>
                <Text style={styles.cardTitle}>Motor Details & Data Upload</Text>

                {/* Motor Type */}
                <View style={styles.inputGroup}>
                    <Text style={styles.label}>Motor Type</Text>
                    <View style={styles.pickerContainer}>
                        <Picker
                            selectedValue={motorType}
                            onValueChange={setMotorType}
                            style={styles.picker}
                            dropdownIconColor={theme.colors.text}>
                            <Picker.Item label="Select Motor Type" value="" />
                            {MOTOR_TYPES.map(type => (
                                <Picker.Item key={type.value} label={type.label} value={type.value} />
                            ))}
                        </Picker>
                    </View>
                </View>

                {/* Phase Type */}
                <View style={styles.inputGroup}>
                    <Text style={styles.label}>Phase</Text>
                    <View style={styles.pickerContainer}>
                        <Picker
                            selectedValue={phaseType}
                            onValueChange={setPhaseType}
                            style={styles.picker}
                            dropdownIconColor={theme.colors.text}>
                            <Picker.Item label="Select Phase" value="" />
                            {PHASE_TYPES.map(type => (
                                <Picker.Item key={type.value} label={type.label} value={type.value} />
                            ))}
                        </Picker>
                    </View>
                </View>

                {/* HP Input */}
                <View style={styles.inputGroup}>
                    <Text style={styles.label}>Horsepower (HP)</Text>
                    <TextInput
                        style={styles.input}
                        placeholder="e.g., 7.5"
                        placeholderTextColor={theme.colors.textSecondary}
                        keyboardType="numeric"
                        value={hp}
                        onChangeText={setHp}
                    />
                </View>

                {/* Voltage */}
                <View style={styles.inputGroup}>
                    <Text style={styles.label}>Voltage (V)</Text>
                    <View style={styles.pickerContainer}>
                        <Picker
                            selectedValue={voltage}
                            onValueChange={setVoltage}
                            style={styles.picker}
                            dropdownIconColor={theme.colors.text}>
                            <Picker.Item label="Select Voltage" value="" />
                            {VOLTAGES.map(v => (
                                <Picker.Item key={v.value} label={v.label} value={v.value} />
                            ))}
                        </Picker>
                    </View>
                </View>

                {/* File Upload */}
                <View style={styles.inputGroup}>
                    <Text style={styles.label}>Upload CSV Data</Text>
                    <TouchableOpacity style={styles.fileButton} onPress={pickDocument}>
                        <Text style={styles.fileButtonText}>
                            {csvFile ? `✓ ${csvFile.name}` : '📁 Choose CSV File'}
                        </Text>
                    </TouchableOpacity>
                    <Text style={styles.fileNote}>
                        CSV should contain 'Vibration X/Y/Z (mm/s)' and 'MLX90393 X/Y/Z (mT)' columns
                    </Text>
                </View>

                {/* Submit Button */}
                <TouchableOpacity
                    style={[styles.submitButton, loading && styles.submitButtonDisabled]}
                    onPress={handleAnalyze}
                    disabled={loading}>
                    {loading ? (
                        <ActivityIndicator color="#fff" />
                    ) : (
                        <Text style={styles.submitButtonText}>📊 Analyze Motor</Text>
                    )}
                </TouchableOpacity>
            </View>
        </ScrollView>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: theme.colors.background,
    },
    header: {
        padding: theme.spacing.lg,
        paddingTop: theme.spacing.xl,
    },
    title: {
        fontSize: theme.fontSize.xxl,
        fontWeight: 'bold',
        color: theme.colors.text,
        marginBottom: theme.spacing.sm,
    },
    subtitle: {
        fontSize: theme.fontSize.md,
        color: theme.colors.textSecondary,
        lineHeight: 22,
    },
    card: {
        backgroundColor: theme.colors.surface,
        margin: theme.spacing.md,
        padding: theme.spacing.lg,
        borderRadius: theme.borderRadius.lg,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.3,
        shadowRadius: 8,
        elevation: 5,
    },
    cardTitle: {
        fontSize: theme.fontSize.lg,
        fontWeight: '600',
        color: theme.colors.text,
        marginBottom: theme.spacing.lg,
    },
    inputGroup: {
        marginBottom: theme.spacing.lg,
    },
    label: {
        fontSize: theme.fontSize.md,
        color: theme.colors.text,
        marginBottom: theme.spacing.sm,
        fontWeight: '500',
    },
    pickerContainer: {
        backgroundColor: theme.colors.background,
        borderRadius: theme.borderRadius.sm,
        borderWidth: 1,
        borderColor: theme.colors.border,
    },
    picker: {
        color: theme.colors.text,
        height: 50,
    },
    input: {
        backgroundColor: theme.colors.background,
        borderRadius: theme.borderRadius.sm,
        borderWidth: 1,
        borderColor: theme.colors.border,
        padding: theme.spacing.md,
        color: theme.colors.text,
        fontSize: theme.fontSize.md,
    },
    fileButton: {
        backgroundColor: theme.colors.primary,
        padding: theme.spacing.md,
        borderRadius: theme.borderRadius.sm,
        alignItems: 'center',
    },
    fileButtonText: {
        color: '#fff',
        fontSize: theme.fontSize.md,
        fontWeight: '600',
    },
    fileNote: {
        fontSize: theme.fontSize.xs,
        color: theme.colors.textSecondary,
        marginTop: theme.spacing.sm,
        fontStyle: 'italic',
    },
    submitButton: {
        backgroundColor: theme.colors.secondary,
        padding: theme.spacing.lg,
        borderRadius: theme.borderRadius.md,
        alignItems: 'center',
        marginTop: theme.spacing.md,
    },
    submitButtonDisabled: {
        opacity: 0.6,
    },
    submitButtonText: {
        color: '#fff',
        fontSize: theme.fontSize.lg,
        fontWeight: 'bold',
    },
});

export default HomeScreen;
