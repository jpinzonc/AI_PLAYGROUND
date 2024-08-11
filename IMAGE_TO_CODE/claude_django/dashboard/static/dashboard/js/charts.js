document.addEventListener('DOMContentLoaded', function() {
    createCostChart();
    createPhaseChart();
    createCompletionChart();
});

function createCostChart() {
    const ctx = document.getElementById('costChart').getContext('2d');
    const totalBudget = 93332; // Get this from your Django context
    const actualCost = 48048; // Get this from your Django context
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
            }, {
                data: [0.1, 99.9], // Needle
                backgroundColor: [
                    'rgba(255, 255, 255, 1)',
                    'rgba(0, 0, 0, 0)'
                ],
                borderWidth: 0,
                circumference: 180,
                rotation: 270 + (percentage * 1.8)
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
}

function createPhaseChart() {
    const ctx = document.getElementById('phaseChart').getContext('2d');
    const phaseHours = {
        'Closure Stage': 5,
        'Execution Stage': 164,
        'Monitor & Control': 36,
        'Project Initiation Stage': 40,
        'Project Planning Stage': 144
    };

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(phaseHours),
            datasets: [{
                data: Object.values(phaseHours),
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
    const phaseCompletion = {
        'Project Planning Stage': 80.0,
        'Project Initiation Stage': 100.0,
        'Monitor & Control': 11.3,
        'Execution Stage': 8.0,
        'Closure Stage': 0.7
    };

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: Object.keys(phaseCompletion),
            datasets: [{
                data: Object.values(phaseCompletion),
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