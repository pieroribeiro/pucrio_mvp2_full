(function($) {
  'use strict';

  const api_host = "http://localhost"
  const api_host_port = "3002"

  const formatCurrency = (lang = 'pt-BR', coin= 'BRL', value = 0) => {
    return new Intl.NumberFormat(lang, { style: "currency", currency: coin, minimumFractionDigits: 2, maximumFractionDigits: 2}).format(value)
  }

  const formatPercent = (val) => {
    return new Intl.NumberFormat('pt-BR', { style: "percent", minimumFractionDigits: 2, maximumFractionDigits: 2, signDisplay: "exceptZero" }).format(val)    
  }

  const formatDatetime = (val) => {
    const d = new Date(val)
    return `${d.getDate()}/${d.getMonth()}/${d.getFullYear()} às ${d.getHours()}:${d.getMinutes()}`
  }

  const calculateIncrement = (valueBefore, valueAfter) => {
    valueBefore = parseFloat(valueBefore)
    valueAfter = parseFloat(valueAfter)
    return ((valueAfter - valueBefore) / valueBefore)
  }

  const loadGraph = (container, data) => {
    const marketingOverviewCanvas = document.getElementById(container);
    new Chart(marketingOverviewCanvas, {
      type: 'line',
      data: {
        datasets: [{
          label: 'Valores',
          data: data,
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          borderWidth: 0.5,
          borderColor: 'rgba(75, 192, 192, 0.6)',
          fill: true,
          tension: 0.4
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            display: false,
          }
        }
      }
    });
  }

  $(function() {
    if ($("#card-bitcoin").length) {
      fetch(`${api_host}:${api_host_port}/api/finance/BTC-USD`, {headers: {"accept": "application/json", "Content-type": "application/json"}})
        .then(res => res.json())
        .then(res => {
          const data = res.results.map(item => parseFloat(item.value))
          const graphData = res.results.map(item => {return {x: item.created_at, y: parseFloat(item.value)}})

          $("#card-bitcoin .marketingOverview-value").text(formatCurrency('en-US', 'USD', data[data.length - 1]))
          if (data[data.length - 2]) {   
            const value = calculateIncrement(data[data.length - 2], data[data.length - 1])
            if (value > 0) {
              $("#card-bitcoin .marketingOverview-value-increment").text(`(${formatPercent(value)})`)
              $("#card-bitcoin .marketingOverview-value-increment").removeClass("text-danger").addClass('text-success')
            } else if (value < 0) {
              $("#card-bitcoin .marketingOverview-value-increment").text(`(${formatPercent(value)})`)
              $("#card-bitcoin .marketingOverview-value-increment").removeClass("text-success").addClass('text-danger')
            } else {
              $("#card-bitcoin .marketingOverview-value-increment").text("")
              $("#card-bitcoin .marketingOverview-value-increment").removeClass("text-success").removeClass('text-danger')
            }
          }
          
          loadGraph("marketingOverview-bitcoin", graphData)
          console.log(`BITCOIN: ${JSON.stringify(graphData)}`)
        })
        .catch(e => {
          console.error('Erro ao carregar dados de BITCOIN', `Message: ${e.message}`)
        })
    }

    if ($("#card-ethereum").length) {
      fetch(`${api_host}:${api_host_port}/api/finance/ETH-USD`, {headers: {"accept": "application/json", "Content-type": "application/json"}})
        .then(res => res.json())
        .then(res => {
          const data = res.results.map(item => item.value)
          const graphData = res.results.map(item => {return {x: item.created_at, y: parseFloat(item.value)}})

          $("#card-ethereum .marketingOverview-value").text(formatCurrency('en-US', 'USD', data[data.length - 1]))
          if (data[data.length - 2]) {     
            const value = calculateIncrement(data[data.length - 2], data[data.length - 1])
            if (value > 0) {
              $("#card-ethereum .marketingOverview-value-increment").text(`(${formatPercent(value)})`)
              $("#card-ethereum .marketingOverview-value-increment").removeClass("text-danger").addClass('text-success')
            } else if (value < 0) {
              $("#card-ethereum .marketingOverview-value-increment").text(`(${formatPercent(value)})`)
              $("#card-ethereum .marketingOverview-value-increment").removeClass("text-success").addClass('text-danger')
            } else {
              $("#card-ethereum .marketingOverview-value-increment").text("")
              $("#card-ethereum .marketingOverview-value-increment").removeClass("text-success").removeClass('text-danger')
            }
          }

          loadGraph("marketingOverview-ethereum", graphData)
        })
        .catch(e => {
          console.error('Erro ao carregar dados de ETHEREUM', `Message: ${e.message}`)
        })
    }

    if ($("#card-solana").length) {
      fetch(`${api_host}:${api_host_port}/api/finance/SOL-USD`, {headers: {"accept": "application/json", "Content-type": "application/json"}})
        .then(res => res.json())
        .then(res => {
          const data = res.results.map(item => item.value)
          const graphData = res.results.map(item => {return {x: item.created_at, y: parseFloat(item.value)}})

          $("#card-solana .marketingOverview-value").text(formatCurrency('en-US', 'USD', data[data.length - 1]))
          if (data[data.length - 2]) {          
            const value = calculateIncrement(data[data.length - 2], data[data.length - 1])
            if (value > 0) {
              $("#card-solana .marketingOverview-value-increment").text(`(${formatPercent(value)})`)
              $("#card-solana .marketingOverview-value-increment").removeClass("text-danger").addClass('text-success')
            } else if (value < 0) {
              $("#card-solana .marketingOverview-value-increment").text(`(${formatPercent(value)})`)
              $("#card-solana .marketingOverview-value-increment").removeClass("text-success").addClass('text-danger')
            } else {
              $("#card-solana .marketingOverview-value-increment").text("")
              $("#card-solana .marketingOverview-value-increment").removeClass("text-success").removeClass('text-danger')
            }
          }

          loadGraph("marketingOverview-solana", graphData)
        })
        .catch(e => {
          console.error('Erro ao carregar dados de SOLANA', `Message: ${e.message}`)
        })
    }    

    if ($("#card-dollar").length) {
      fetch(`${api_host}:${api_host_port}/api/finance/USD`, {headers: {"accept": "application/json", "Content-type": "application/json"}})
        .then(res => res.json())
        .then(res => {
          const data = res.results.map(item => item.value)
          const graphData = res.results.map(item => {return {x: item.created_at, y: parseFloat(item.value)}})

          $("#card-dollar .marketingOverview-value").text(formatCurrency('pt-BR', 'BRL', data[data.length - 1]))
          if (data[data.length - 2]) {            
            const value = calculateIncrement(data[data.length - 2], data[data.length - 1])
            if (value > 0) {
              $("#card-dollar .marketingOverview-value-increment").text(`(${formatPercent(value)})`)
              $("#card-dollar .marketingOverview-value-increment").removeClass("text-danger").addClass('text-success')
            } else if (value < 0) {
              $("#card-dollar .marketingOverview-value-increment").text(`(${formatPercent(value)})`)
              $("#card-dollar .marketingOverview-value-increment").removeClass("text-success").addClass('text-danger')
            } else {
              $("#card-dollar .marketingOverview-value-increment").text("")
              $("#card-dollar .marketingOverview-value-increment").removeClass("text-success").removeClass('text-danger')
            }
          }
          
          loadGraph("marketingOverview-dollar", graphData)
        })
        .catch(e => {
          console.error('Erro ao carregar dados de DOLLAR', `Message: ${e.message}`)
        })
    }    

    if ($("#card-euro").length) {
      fetch(`${api_host}:${api_host_port}/api/finance/EUR`, {headers: {"accept": "application/json", "Content-type": "application/json"}})
        .then(res => res.json())
        .then(res => {
          const data = res.results.map(item => item.value)
          const graphData = res.results.map(item => {return {x: item.created_at, y: parseFloat(item.value)}})

          $("#card-euro .marketingOverview-value").text(formatCurrency('pt-BR', 'BRL', data[data.length - 1]))
          if (data[data.length - 2]) {
            const value = calculateIncrement(data[data.length - 2], data[data.length - 1])
            if (value > 0) {
              $("#card-euro .marketingOverview-value-increment").text(`(${formatPercent(value)})`)
              $("#card-euro .marketingOverview-value-increment").removeClass("text-danger").addClass('text-success')
            } else if (value < 0) {
              $("#card-euro .marketingOverview-value-increment").text(`(${formatPercent(value)})`)
              $("#card-euro .marketingOverview-value-increment").removeClass("text-success").addClass('text-danger')
            } else {
              $("#card-euro .marketingOverview-value-increment").text("")
              $("#card-euro .marketingOverview-value-increment").removeClass("text-success").removeClass('text-danger')
            }
          }
          
          loadGraph("marketingOverview-euro", graphData)
        })
        .catch(e => {
          console.error('Erro ao carregar dados de EURO', `Message: ${e.message}`)
        })
    }

    if ($("#card-canadianDollar").length) {
      fetch(`${api_host}:${api_host_port}/api/finance/CAD`, {headers: {"accept": "application/json", "Content-type": "application/json"}})
        .then(res => res.json())
        .then(res => {
          const data = res.results.map(item => item.value)
          const graphData = res.results.map(item => {return {x: item.created_at, y: parseFloat(item.value)}})

          $("#card-canadianDollar .marketingOverview-value").text(formatCurrency('pt-BR', 'BRL', data[data.length - 1]))
          if (data[data.length - 2]) {
            const value = calculateIncrement(data[data.length - 2], data[data.length - 1])
            if (value > 0) {
              $("#card-canadianDollar .marketingOverview-value-increment").text(`(${formatPercent(value)})`)
              $("#card-canadianDollar .marketingOverview-value-increment").removeClass("text-danger").addClass('text-success')
            } else if (value < 0) {
              $("#card-canadianDollar .marketingOverview-value-increment").text(`(${formatPercent(value)})`)
              $("#card-canadianDollar .marketingOverview-value-increment").removeClass("text-success").addClass('text-danger')
            } else {
              $("#card-canadianDollar .marketingOverview-value-increment").text("")
              $("#card-canadianDollar .marketingOverview-value-increment").removeClass("text-success").removeClass('text-danger')
            }
          }
          
          loadGraph("marketingOverview-canadianDollar", graphData)
        })
        .catch(e => {
          console.error('Erro ao carregar dados de CANADIAN DOLLAR', `Message: ${e.message}`)
        })
    }  
    
    if ($("#card-news").length) {
      fetch(`${api_host}:${api_host_port}/api/news`, {headers: {"accept": "application/json", "Content-type": "application/json"}})
        .then(res => res.json())
        .then(res => {
          if (res && res.results) {
            res.results.forEach(item => {
              $("#card-news .bullet-line-list").append(`
              <li>
                <div class="d-flex justify-content-between">
                  <div><span class="text-light-green"><a href="${item.url}" target="_blank">${item.title}</a></div>
                  <p>${formatDatetime(item.published_at)}</p>
                </div>
              </li>
              `)
            })
          }          
        })
        .catch(e => {
          console.error('Erro ao carregar Noticias', `Message: ${e.message}`)
        })
    } 
    
    if ($("#card-apis").length) {
      fetch(`${api_host}:${api_host_port}/api`, {headers: {"accept": "application/json", "Content-type": "application/json"}})
        .then(res => res.json())
        .then(res => {
          if (res && res.results) {
            $("#card-apis #list-records").append(`
            <li>
              <div class="row">
                <div class="col-lg-4 d-flex flex-column"><strong>Nome</strong></div>
                <div class="col-lg-4 d-flex flex-column"><strong>URL</strong></div>
                <div class="col-lg-2 d-flex flex-column"><strong>Data de Cadastro</strong></div>
                <div class="col-lg-2 d-flex flex-column"><strong>Ações</strong></div>
              </div>
            </li>
            `)            
            res.results.forEach(item => {
              $("#card-apis #list-records").append(`
              <li>
                <div class="row">
                  <div class="col-lg-4 d-flex flex-column">
                    <span class="text-light-green">${item.name}</span>
                  </div>
                  <div class="col-lg-4 d-flex flex-column">
                    <span class="text-light-red">${item.url}</span>
                  </div>
                  <div class="col-lg-2 d-flex flex-column">
                    <p>${formatDatetime(item.created_at)}</p>
                  </div>
                  <div class="col-lg-2 d-flex flex-column">
                    <div>
                      <button type="button" class="btn btn-warning" data-action="edit-record" data-id="${item.id}" data-toggle="modal" data-target="#modal-admin">Editar</button>
                      <button type="button" class="btn btn-danger" data-action="delete-record" data-id="${item.id}" data-name="${item.name}">Excluir</button>
                    </div>
                  </div>
                </div>
              </li>
              `)
            })

            $('button[data-action="edit-record"]').click((e) => {
              e.stopPropagation();
              e.preventDefault();
              $("#modal-admin").modal("show")
            })

            $('button[data-action="close-modal"]').click((e) => {
              e.stopPropagation();
              e.preventDefault();
              $("#modal-admin").modal("hide")
            })

            $('button[data-action="delete-record"]').click((e) => {
              const data = e.target.dataset
              if (confirm(`Deseja realmente excluir a API ${data["name"]}?`)) {
                fetch(`${api_host}:${api_host_port}/api/${data["id"]}`, {method: 'DELETE', headers: {"accept": "application/json", "Content-type": "application/json"}})
                  .then(res => res.json())
                  .then(res => {
                    if (res && res.status && res.id && res.status === 'DELETED' && res.id > 0) {
                      showAlert(`A API ${data["name"]} (${res.id}) foi excluída.`, 'success')
                    } else {
                      showAlert(`A Api ${data["name"]} não encontrada para ser excluída.`, 'warning')
                    }
                  })
                  .catch(e => {
                    showAlert(`Houve um problema ao tentar excluir a API. Erro: ${e.message}`, 'danger')
                  })
              }
            })
          }          
        })
        .catch(e => {
          console.error('Erro ao carregar APIs', `Message: ${e.message}`)
        })
    }
  });
})(jQuery);
