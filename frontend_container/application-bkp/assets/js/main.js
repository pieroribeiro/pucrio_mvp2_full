const data = {
    labels: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho'],
    datasets: [{
      label: 'Meu Dataset',
      data: [12, 19, 3, 5, 2, 3],
      fill: false,
      borderColor: 'rgb(75, 192, 192)',
      tension: 0.1
    }]
  };

  // Configurações do gráfico
  const config = {
    type: 'line',
    data: data,
    options: {
      scales: {
        x: {
          display: true,
          title: {
            display: true,
            text: 'Meses'
          }
        },
        y: {
          display: true,
          title: {
            display: true,
            text: 'Valores'
          }
        }
      }
    }
  };

  // Criação do gráfico
  var myChart = new Chart(
    document.getElementById('myChart'),
    config
  );