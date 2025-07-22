function initCharts(weightData, heartRateData) {
    // Weight Chart
    const weightCtx = document.getElementById('weightChart').getContext('2d');
    new Chart(weightCtx, {
        type: 'line',
        data: weightData,
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                }
            },
            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    });
    
    // Heart Rate Chart
    const heartRateCtx = document.getElementById('heartRateChart').getContext('2d');
    new Chart(heartRateCtx, {
        type: 'line',
        data: heartRateData,
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                }
            },
            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    });
    
    // Time range selector functionality
    document.querySelectorAll('.time-range-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const range = this.getAttribute('data-range');
            fetchHealthData(range);
        });
    });
    
    // Fetch health data for a specific time range
    function fetchHealthData(range) {
        fetch(`/get_health_data?range=${range}`)
        .then(response => response.json())
        .then(data => {
            // Update charts with new data
            updateChart('weightChart', data.dates, data.weights, 'Weight (kg)');
            updateChart('heartRateChart', data.dates, data.heart_rates, 'Heart Rate (bpm)');
        });
    }
    
    // Helper function to update a chart
    function updateChart(chartId, labels, data, label) {
        const chart = Chart.getChart(chartId);
        chart.data.labels = labels;
        chart.data.datasets[0].data = data;
        chart.data.datasets[0].label = label;
        chart.update();
    }
}
