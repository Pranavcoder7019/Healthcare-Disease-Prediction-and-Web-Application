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
// Dark Mode Toggle
const toggleBtn = document.getElementById('darkModeToggle');
if (toggleBtn) {
    toggleBtn.addEventListener('click', () => {
        const theme = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
    });
}
