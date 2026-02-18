// Budget Dashboard Chart JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('departmentChart');
    
    if (ctx) {
        // Get data from data attributes or window object
        const labels = window.departmentLabels || [];
        const data = window.departmentData || [];
        
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: ['#1e3a8a', '#f59e0b', '#059669', '#dc2626', '#6366f1']
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }
});
