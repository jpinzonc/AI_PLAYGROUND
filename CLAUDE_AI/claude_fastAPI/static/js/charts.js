document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/project-data')
        .then(response => response.json())
        .then(data => {
            console.log('Received data:', data);  // Add this line for debugging
            createCostChart(data.total_budget, data.actual_cost);
            createPhaseChart(data.phase_hours);
            createCompletionChart(data.phase_completion);
        })
        .catch(error => console.error('Error fetching project data:', error));
});

function createCostChart(totalBudget, actualCost) {
    const ctx = document.getElementById('costChart').getContext('2d');
    if (!ctx) {
        console.error('Could not find costChart element');
        return;
    }
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

function createPhaseChart(phaseHours) {
    const ctx = document.getElementById('phaseChart').getContext('2d');
    if (!ctx) {
        console.error('Could not find phaseChart element');
        return;
    }
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

function createCompletionChart(phaseCompletion) {
    const ctx = document.getElementById('completionChart').getContext('2d');
    if (!ctx) {
        console.error('Could not find completionChart element');
        return;
    }
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