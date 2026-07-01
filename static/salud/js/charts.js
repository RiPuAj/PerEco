(function () {
  if (typeof Chart === 'undefined') return;

  const data = window.SALUD_CHART_DATA || { weight: { labels: [], values: [] }, kcal: { labels: [], values: [] } };

  const weightCanvas = document.getElementById('weightChart');
  if (weightCanvas && data.weight.labels.length && data.weight.values.length) {
    new Chart(weightCanvas, {
      type: 'line',
      data: {
        labels: data.weight.labels,
        datasets: [{
          label: 'Peso (kg)',
          data: data.weight.values,
          borderColor: '#1f8a5f',
          backgroundColor: 'rgba(31, 138, 95, 0.1)',
          tension: 0.3,
          fill: true,
          pointRadius: 3,
          spanGaps: false,
        }],
      },
      options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: { y: { ticks: { callback: (v) => v + ' kg' } } },
      },
    });
  }

  const kcalCanvas = document.getElementById('kcalChart');
  if (kcalCanvas && data.kcal.labels.length && data.kcal.values.length) {
    new Chart(kcalCanvas, {
      type: 'bar',
      data: {
        labels: data.kcal.labels,
        datasets: [{
          label: 'Kcal',
          data: data.kcal.values,
          backgroundColor: '#197349',
          borderRadius: 6,
        }],
      },
      options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: { y: { ticks: { callback: (v) => v + ' kcal' } } },
      },
    });
  }
})();
