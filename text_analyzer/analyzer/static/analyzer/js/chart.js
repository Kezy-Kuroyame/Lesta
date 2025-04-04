document.addEventListener('DOMContentLoaded', function () {
    const ctx = document.getElementById('tfidfChart');
    if (!ctx) return;

    try {
        const labels = JSON.parse(document.getElementById('chart-labels').textContent);
        const data = JSON.parse(document.getElementById('chart-data').textContent);

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'TF-IDF (Топ-10 слов)',
                    data: data,
                    backgroundColor: 'rgba(75, 192, 192, 0.6)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Значение TF-IDF'
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error("Ошибка при разборе JSON:", error);
    }
});
