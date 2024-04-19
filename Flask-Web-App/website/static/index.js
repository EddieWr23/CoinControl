function deleteIncome(incomeId) {
  fetch("/delete-income", {
    method: "POST",
    body: JSON.stringify({ incomeId: incomeId }),
    headers: {
      'Content-Type': 'application/json'
    }
  }).then((_res) => {
    window.location.href = "/";
  });
}

function deleteExpense(expenseId) {
  fetch("/delete-expense", {
    method: "POST",
    body: JSON.stringify({ expenseId: expenseId }),
    headers: {
      'Content-Type': 'application/json'
    }
  }).then((_res) => {
    window.location.href = "/";
  });
}

function createChart(dates, balance) {
  var ctx = document.getElementById('myChart').getContext('2d');
  var myChart = new Chart(ctx, {
      type: 'line',
      data: {
          labels: dates,  // This will be the dates
          datasets: [{
              label: 'Balance',
              data: balance,  // This will be the balance
              backgroundColor: '#007bff',
              borderColor: '#007bff',
              borderWidth: 1
          }]
      },
      options: {
          scales: {
              y: {
                  beginAtZero: false
              }
          },
          responsive: true
      }
  });
}


