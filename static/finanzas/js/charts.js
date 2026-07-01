(function () {
  if (typeof Chart === 'undefined') return;

  const data = window.FINANZAS_CHART_DATA || { expense_cat: { labels: [], values: [], colors: [] } };

  const catCanvas = document.getElementById('expenseCategoryChart');
  if (catCanvas && data.expense_cat.labels.length && data.expense_cat.values.length) {
    new Chart(catCanvas, {
      type: 'doughnut',
      data: {
        labels: data.expense_cat.labels,
        datasets: [{
          data: data.expense_cat.values,
          backgroundColor: data.expense_cat.colors,
          borderWidth: 2,
          borderColor: '#fff',
        }],
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'bottom',
            labels: { padding: 16, usePointStyle: true, pointStyle: 'circle' },
          },
        },
      },
    });
  }
})();