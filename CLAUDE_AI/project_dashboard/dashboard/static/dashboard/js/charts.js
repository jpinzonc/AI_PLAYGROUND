document.addEventListener('DOMContentLoaded', function() {
    createCostChart();
    createPhaseChart();
    createCompletionChart();
});

function createCostChart() {
    const ctx = document.getElementById('costChart').getContext('2d');
    const totalBudget = 93332;
    const actualCost = 48048;
    const percentage = (actualCost / totalBudget) * 100;

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [percentage, 100 - percentage],
                backgroundColor: [
                    'rgba(0, 255, 0, 0.8)',
                    'rgba(211, 211, 211, 0.3)'
                ],
                borderWidth: 0,
                circumference: 180,
                rotation: 270
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '80%',
            plugins: {
                tooltip: { enabled: false },
                legend: { display: false }
            }
        }
    });

    // Add needle
    const needleValue = percentage * 1.8 - 90;
    const needle = new Chart(ctx, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [1, 99],
                backgroundColor: ['rgba(255, 255, 255, 1)', 'rgba(0, 0, 0, 0)'],
                borderWidth: 0,
                circumference: 1,
                rotation: needleValue
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '95%',
            plugins: {
                tooltip: { enabled: false },
                legend: { display: false }
            }
        }
    });
}

function createPhaseChart() {
    const ctx = document.getElementById('phaseChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Closure Stage', 'Execution Stage', 'Monitor & Control', 'Project Initiation Stage', 'Project Planning Stage'],
            datasets: [{
                data: [5, 164, 36, 40, 144],
                backgroundColor: 'rgba(54, 162, 235, 0.8)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: { color: 'white' }
                },
                y: {
                    grid: {
                        display: false
                    },
                    ticks: { color: 'white' }
                }
            }
        }
    });
}

function createCompletionChart() {
    const ctx = document.getElementById('completionChart').getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Project Planning Stage', 'Project Initiation Stage', 'Monitor & Control', 'Execution Stage', 'Closure Stage'],
            datasets: [{
                data: [80, 100, 11.3, 8, 0.7],
                backgroundColor: [
                    'rgba(54, 162, 235, 0.8)',
                    'rgba(255, 206, 86, 0.8)',
                    'rgba(75, 192, 192, 0.8)',
                    'rgba(153, 102, 255, 0.8)',
                    'rgba(255, 99, 132, 0.8)'
                ],
                borderColor: 'rgba(255, 255, 255, 0.1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        color: 'white'
                    }
                }
            }
        }
    });
}