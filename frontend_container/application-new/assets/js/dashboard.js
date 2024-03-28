(function($) {
  'use strict';

  const loadGraph = (container, labels, data) => {
    const marketingOverviewCanvas = document.getElementById(container);
      new Chart(marketingOverviewCanvas, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [{
            label: 'This week',
            data: data,
            backgroundColor: "#1F3BB3",
            borderColor: [
                '#1F3BB3',
            ],
            borderWidth: 0,
              barPercentage: 0.35,
              fill: true, // 3: no fill
          }]
        },
        options: {
          legend: {
            display: false
          },
          tooltips: {
            enabled: false
          },
          responsive: true,
          maintainAspectRatio: false,
          elements: {
            line: {
                tension: 0.4,
            }
          },        
          scales: {
            yAxes: {
              grid: {
                display: true,
                drawTicks: false,
                color:"#F0F0F0",
                zeroLineColor: '#F0F0F0',
              },
              ticks: {
                beginAtZero: false,
                autoSkip: true,
                maxTicksLimit: 4,
                color:"#6B778C",
                font: {
                  size: 10,
                }
              }
            },
            xAxes: {
              stacked: true,
              grid: {
                display: false,
                drawTicks: false,
              },
              ticks: {
                beginAtZero: false,
                autoSkip: true,
                maxTicksLimit: 7,
                color:"#6B778C",
                font: {
                  size: 10,
                }
              }
            }
          }
        }
      });
  }

  $(function() {
    if ($("#marketingOverview-bitcoin").length) {
      fetch('http://api_host:3002/api/finance/BTC-USD', {})
        .then(res => res.json())
        .then(res => {
          const labels = []
          const data = []
          loadGraph("marketingOverview-bitcoin", labels, data)
        })
        .catch(e => {
          console.error('Erro ao carregar dados de BITCOIN', `Message: ${e.message}`)
        })
    }

    if ($("#marketingOverview-ethereum").length) {
      fetch('http://api_host:3002/api/finance/ETH-USD', {})
        .then(res => res.json())
        .then(res => {
          const labels = []
          const data = []
          loadGraph("marketingOverview-ethereum", labels, data)
        })
        .catch(e => {
          console.error('Erro ao carregar dados de ETHEREUM', `Message: ${e.message}`)
        })
    }

    if ($("#marketingOverview-solana").length) {
      fetch('http://api_host:3002/api/finance/SOL-USD', {})
        .then(res => res.json())
        .then(res => {
          const labels = []
          const data = []
          loadGraph("marketingOverview-solana", labels, data)
        })
        .catch(e => {
          console.error('Erro ao carregar dados de SOLANA', `Message: ${e.message}`)
        })
    }    

    if ($("#marketingOverview-dollar").length) {
      fetch('http://api_host:3002/api/finance/USD', {})
        .then(res => res.json())
        .then(res => {
          const labels = []
          const data = []
          loadGraph("marketingOverview-dollar", labels, data)
        })
        .catch(e => {
          console.error('Erro ao carregar dados de DOLLAR', `Message: ${e.message}`)
        })
    }    

    if ($("#marketingOverview-euro").length) {
      fetch('http://api_host:3002/api/finance/EUR', {})
        .then(res => res.json())
        .then(res => {
          const labels = []
          const data = []
          loadGraph("marketingOverview-euro", labels, data)
        })
        .catch(e => {
          console.error('Erro ao carregar dados de EURO', `Message: ${e.message}`)
        })
    }

    if ($("#marketingOverview-canadianDollar").length) {
      fetch('http://api_host:3002/api/finance/CAD', {})
        .then(res => res.json())
        .then(res => {
          const labels = []
          const data = []
          loadGraph("marketingOverview-canadianDollar", labels, data)
        })
        .catch(e => {
          console.error('Erro ao carregar dados de CANADIAN DOLLAR', `Message: ${e.message}`)
        })
    }    
  });
})(jQuery);