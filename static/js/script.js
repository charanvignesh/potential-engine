/**
 * Plots a line chart using Plotly.
 * @param {string} divId - The ID of the div element to plot in.
 * @param {Array<number>} xData - The X-axis data.
 * @param {Array<Array<number>>} yDataList - A list of Y-axis data arrays (for multiple traces).
 * @param {Array<string>} labels - A list of trace names.
 * @param {string} title - The title of the plot.
 * @param {string} yLabel - The Y-axis label.
 */
function plotLine(divId, xData, yDataList, labels, title, yLabel) {
    let traces = [];
    // Using a professional, accessible color palette
    const colors = ['#00a896', '#004c6d', '#ff6f61', '#f9c74f', '#9b59b6'];
    
    // Determine line width based on plot type for clarity
    const lineWidth = divId.includes('psd') ? 1.5 : 1; 

    for(let i = 0; i < yDataList.length; i++){
        traces.push({
            x: xData, 
            y: yDataList[i], 
            mode: 'lines', 
            name: labels[i],
            line: { color: colors[i % colors.length], width: lineWidth } 
        });
    }
    
    let layout = {
        title: { text: title, font: { size: 18, family: 'Montserrat' } },
        xaxis: { 
            title: divId.includes('psd') ? 'Frequency (Hz)' : 'Sample', 
            showgrid: true,
            linecolor: '#ccc'
        },
        yaxis: { 
            title: yLabel,
            zeroline: true,
            linecolor: '#ccc'
        },
        margin: { t: 60, l: 60, r: 20, b: 60 }, // Increased margins for clarity
        hovermode: 'x unified', // Better for time series
        plot_bgcolor: '#ffffff', // White plot background
        paper_bgcolor: 'white', 
        legend: { 
            orientation: 'h', 
            y: 1.15, 
            yanchor: 'top',
            font: { size: 12 }
        }
    };
    

    Plotly.newPlot(divId, traces, layout, { responsive: true, displayModeBar: false });
}

/**
 * Plots a heatmap using Plotly.
 * @param {string} divId - The ID of the div element to plot in.
 * @param {Array<Array<number>>} zData - The matrix of data values.
 * @param {Array<string>} xLabels - The X-axis labels (feature names).
 * @param {Array<string>} yLabels - The Y-axis labels.
 * @param {string} title - The title of the plot.
 */
function plotHeatmap(divId, zData, xLabels, yLabels, title){
    let data = [{
        z: zData, 
        x: xLabels, 
        y: yLabels, 
        type: 'heatmap', 
        colorscale: 'Viridis', // Professional colorscale
        reversescale: false,
        colorbar: {
            title: 'Feature Value',
            len: 0.5,
            thickness: 20,
            titlefont: { size: 12 }
        }
    }];
    
    let layout = {
        title: { text: title, font: { size: 18, family: 'Montserrat' } },
        margin: { t: 60, l: 150, r: 30, b: 150 }, 
        xaxis: {
            automargin: true, 
            tickangle: -45,
            title: 'Extracted Features'
        },
        yaxis: {
            automargin: true,
            title: 'Data Instance'
        }
    };
    Plotly.newPlot(divId, data, layout, { responsive: true, displayModeBar: false });
}

/**
 * Plots a gauge chart for the Motor Health Score.
 * @param {number} value - The health score (0-100).
 */
function plotHealthGauge(value) {
    const data = [{
        type: 'indicator',
        mode: 'gauge+number',
        value: value,
        domain: { x: [0, 1], y: [0, 1] },
        title: { text: "Health Score (%)", font: { size: 16 } },
        gauge: {
            axis: { range: [null, 100], tickwidth: 1, tickcolor: "#333" },
            bar: { color: "#2c3e50" },
            bgcolor: "white",
            borderwidth: 2,
            bordercolor: "gray",
            steps: [
                { range: [0, 50], color: '#e74c3c' },   // Red/Danger
                { range: [50, 75], color: '#f39c12' },  // Orange/Warning
                { range: [75, 100], color: '#27ae60' } // Green/Good
            ],
        }
    }];

    const layout = {
        margin: { t: 30, b: 10, l: 30, r: 30 },
        paper_bgcolor: "white",
        height: 250,
        autosize: true
    };

    Plotly.newPlot('healthGauge', data, layout, { responsive: true, displayModeBar: false });
}


document.addEventListener('DOMContentLoaded', function() {
    // Check if the dashboard elements exist before plotting
    if (document.getElementById('vibPlot')) {
        plotLine('vibPlot', samples, vibData, ['Vib X','Vib Y','Vib Z'],'Vibration Time Series','mm/s');
        plotLine('magPlot', samples, magData, ['Mag X','Mag Y','Mag Z'],'Magnetic Time Series','mT');
        // Added specific units to PSD labels for clarity
        plotLine('psdVibPlot', f_vib, [P_vib], ['PSD Vib X'],'Power Spectral Density (Vibration X)','Power/Frequency (mm/s)');
        plotLine('psdMagPlot', f_mag, [P_mag], ['PSD Mag X'],'Power Spectral Density (Magnetic X)','Power/Frequency (mT)');
        
        const featVals = [featNames.map(f => features[f])];
        plotHeatmap('heatmapPlot', featVals, featNames, ['Value'],'Analyzed Features Comparison');
        
        plotHealthGauge(healthFrac);
    }
});