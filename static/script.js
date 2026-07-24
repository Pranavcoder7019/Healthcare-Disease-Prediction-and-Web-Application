document.addEventListener('DOMContentLoaded', function() {
    // Canvas setup
    const ctx = document.getElementById('historyChart');
    if (ctx) {
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['January', 'February', 'March', 'April'],
                datasets: [{
                    label: 'Risk Prediction Level',
                    data: [1, 2, 1, 3]
                }]
            }
        });
    }
});