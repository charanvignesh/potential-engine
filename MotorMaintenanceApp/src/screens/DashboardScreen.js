import React from 'react';
import {
    View,
    Text,
    StyleSheet,
    ScrollView,
    TouchableOpacity,
    Dimensions,
} from 'react-native';
import { LineChart } from 'react-native-chart-kit';
import { AnimatedCircularProgress } from 'react-native-circular-progress';
import { theme } from '../styles/theme';

const DashboardScreen = ({ route, navigation }) => {
    const { data } = route.params;
    const { motor_info, prediction, data: sensorData } = data;

    const screenWidth = Dimensions.get('window').width;

    const getHealthColor = () => {
        const health = prediction.health_percentage;
        if (health >= 75) return theme.colors.success;
        if (health >= 25) return theme.colors.warning;
        return theme.colors.danger;
    };

    const getFaultColor = () => {
        const fault = prediction.fault.toLowerCase();
        if (fault.includes('normal')) return theme.colors.success;
        if (fault.includes('bearing')) return theme.colors.warning;
        return theme.colors.danger;
    };

    const chartConfig = {
        backgroundColor: theme.colors.surface,
        backgroundGradientFrom: theme.colors.surface,
        backgroundGradientTo: theme.colors.background,
        decimalPlaces: 2,
        color: (opacity = 1) => `rgba(99, 102, 241, ${opacity})`,
        labelColor: (opacity = 1) => `rgba(241, 245, 249, ${opacity})`,
        style: {
            borderRadius: theme.borderRadius.md,
        },
        propsForDots: {
            r: '2',
            strokeWidth: '1',
            stroke: theme.colors.primary,
        },
    };

    return (
        <ScrollView style={styles.container}>
            <View style={styles.header}>
                <Text style={styles.title}>🔬 Motor Analysis Dashboard</Text>
                <Text style={styles.subtitle}>
                    {motor_info.motor_type} ({motor_info.hp} HP)
                </Text>
            </View>

            {/* Motor Info Card */}
            <View style={styles.card}>
                <Text style={styles.cardTitle}>⚙️ Motor Info</Text>
                <View style={styles.infoRow}>
                    <Text style={styles.infoLabel}>Type:</Text>
                    <Text style={styles.infoValue}>{motor_info.motor_type}</Text>
                </View>
                <View style={styles.infoRow}>
                    <Text style={styles.infoLabel}>Phase:</Text>
                    <Text style={styles.infoValue}>{motor_info.phase_type}</Text>
                </View>
                <View style={styles.infoRow}>
                    <Text style={styles.infoLabel}>HP:</Text>
                    <Text style={styles.infoValue}>{motor_info.hp}</Text>
                </View>
                <View style={styles.infoRow}>
                    <Text style={styles.infoLabel}>Voltage:</Text>
                    <Text style={styles.infoValue}>{motor_info.voltage} V</Text>
                </View>
            </View>

            {/* Prediction Results */}
            <View style={[styles.card, { borderLeftWidth: 4, borderLeftColor: getFaultColor() }]}>
                <Text style={styles.cardTitle}>⚠️ Predicted Fault</Text>
                <Text style={[styles.faultText, { color: getFaultColor() }]}>
                    {prediction.fault}
                </Text>

                <Text style={[styles.cardTitle, { marginTop: theme.spacing.lg }]}>
                    ⏳ Remaining Useful Life (RUL)
                </Text>
                <Text style={styles.rulText}>{prediction.rul}</Text>
                <Text style={styles.deviationText}>
                    Feature Deviation: {prediction.deviation}
                </Text>
            </View>

            {/* Health Gauge */}
            <View style={styles.card}>
                <Text style={styles.cardTitle}>💚 Motor Health Score</Text>
                <View style={styles.gaugeContainer}>
                    <AnimatedCircularProgress
                        size={200}
                        width={20}
                        fill={prediction.health_percentage}
                        tintColor={getHealthColor()}
                        backgroundColor={theme.colors.border}
                        rotation={0}
                        lineCap="round">
                        {() => (
                            <View style={styles.gaugeContent}>
                                <Text style={styles.gaugeValue}>{prediction.health_percentage}%</Text>
                                <Text style={styles.gaugeLabel}>{prediction.health_status.toUpperCase()}</Text>
                            </View>
                        )}
                    </AnimatedCircularProgress>
                </View>
            </View>

            {/* Vibration Chart */}
            <View style={styles.card}>
                <Text style={styles.cardTitle}>📊 Vibration Signals (X-axis)</Text>
                <LineChart
                    data={{
                        labels: [],
                        datasets: [
                            {
                                data: sensorData.vibration.x.slice(0, 50), // Show first 50 points
                            },
                        ],
                    }}
                    width={screenWidth - 64}
                    height={220}
                    chartConfig={chartConfig}
                    bezier
                    style={styles.chart}
                />
            </View>

            {/* Magnetic Chart */}
            <View style={styles.card}>
                <Text style={styles.cardTitle}>🧲 Magnetic Signals (X-axis)</Text>
                <LineChart
                    data={{
                        labels: [],
                        datasets: [
                            {
                                data: sensorData.magnetic.x.slice(0, 50), // Show first 50 points
                            },
                        ],
                    }}
                    width={screenWidth - 64}
                    height={220}
                    chartConfig={{
                        ...chartConfig,
                        color: (opacity = 1) => `rgba(139, 92, 246, ${opacity})`,
                    }}
                    bezier
                    style={styles.chart}
                />
            </View>

            {/* Back Button */}
            <TouchableOpacity
                style={styles.backButton}
                onPress={() => navigation.goBack()}>
                <Text style={styles.backButtonText}>← Analyze Another Motor</Text>
            </TouchableOpacity>

            <View style={{ height: 40 }} />
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
        marginBottom: theme.spacing.md,
    },
    infoRow: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        paddingVertical: theme.spacing.sm,
        borderBottomWidth: 1,
        borderBottomColor: theme.colors.border,
    },
    infoLabel: {
        fontSize: theme.fontSize.md,
        color: theme.colors.textSecondary,
        fontWeight: '500',
    },
    infoValue: {
        fontSize: theme.fontSize.md,
        color: theme.colors.text,
        fontWeight: '600',
    },
    faultText: {
        fontSize: theme.fontSize.xl,
        fontWeight: 'bold',
        textAlign: 'center',
        paddingVertical: theme.spacing.md,
    },
    rulText: {
        fontSize: theme.fontSize.lg,
        color: theme.colors.text,
        textAlign: 'center',
        fontWeight: '600',
        paddingVertical: theme.spacing.sm,
    },
    deviationText: {
        fontSize: theme.fontSize.sm,
        color: theme.colors.textSecondary,
        textAlign: 'center',
        marginTop: theme.spacing.sm,
    },
    gaugeContainer: {
        alignItems: 'center',
        paddingVertical: theme.spacing.lg,
    },
    gaugeContent: {
        alignItems: 'center',
    },
    gaugeValue: {
        fontSize: theme.fontSize.xxl,
        fontWeight: 'bold',
        color: theme.colors.text,
    },
    gaugeLabel: {
        fontSize: theme.fontSize.sm,
        color: theme.colors.textSecondary,
        marginTop: theme.spacing.xs,
    },
    chart: {
        marginVertical: theme.spacing.sm,
        borderRadius: theme.borderRadius.md,
    },
    backButton: {
        backgroundColor: theme.colors.primary,
        margin: theme.spacing.md,
        padding: theme.spacing.lg,
        borderRadius: theme.borderRadius.md,
        alignItems: 'center',
    },
    backButtonText: {
        color: '#fff',
        fontSize: theme.fontSize.md,
        fontWeight: '600',
    },
});

export default DashboardScreen;
