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

  return new Chart(marketingOverviewCanvas, {
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

function loadCoinValues (endpoint, coinType, container, graphicsContainer, formatValueFN, formatIncrementFN) {
  fetch(endpoint, {headers: {"accept": "application/json", "Content-type": "application/json"}})
    .then(res => res.json())
    .then(res => {
      const data = res.results.map(item => parseFloat(item.value))
      const graphData = res.results.map(item => {return {x: item.created_at, y: parseFloat(item.value)}})

      $(`#${container} .marketingOverview-value`).text(formatValueFN((coinType == 'crypto') ? 'en-US' : 'pt-BR', (coinType == 'crypto') ? 'USD' : 'BRL', data[data.length - 1]))
      if (data[data.length - 2]) {   
        const value = calculateIncrement(data[data.length - 2], data[data.length - 1])
        if (value > 0) {
          $(`#${container} .marketingOverview-value-increment`).text(`(${formatIncrementFN(value)})`)
          $(`#${container} .marketingOverview-value-increment`).removeClass("text-danger").addClass('text-success')
        } else if (value < 0) {
          $(`#${container} .marketingOverview-value-increment`).text(`(${formatIncrementFN(value)})`)
          $(`#${container} .marketingOverview-value-increment`).removeClass("text-success").addClass('text-danger')
        } else {
          $(`#${container} .marketingOverview-value-increment`).text("")
          $(`#${container} .marketingOverview-value-increment`).removeClass("text-success").removeClass('text-danger')
        }
      }
      
      loadGraph(graphicsContainer, graphData)
    })
    .catch(e => {
      console.error('Erro ao carregar dados financeiros.', `Message: ${e.message}`)
    })
}

function loadNewsValues () {
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


function loadListAPIs () {
  fetch(`${api_host}:${api_host_port}/api`, {headers: {"accept": "application/json", "Content-type": "application/json"}})
  .then(res => res.json())
  .then(res => {
    $("#card-apis #list-records").empty()
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
              if (res && res.status && res.id && res.status === 'OK' && res.id > 0) {
                showAlert(`A API ${data["name"]} (${res.id}) foi excluída.`, 'success')
                loadListAPIs()
              } else {
                showAlert(`A Api ${data["name"]} não encontrada para ser excluída.`, 'warning')
                loadListAPIs()
              }
            })
            .catch(e => {
              showAlert(`Houve um problema ao tentar excluir a API. Erro: ${e.message}`, 'danger')
              loadListAPIs()
            })
        }
      })
    }          
  })
  .catch(e => {
    console.error('Erro ao carregar APIs', `Message: ${e.message}`)
  })
}

(function($) {
  'use strict';

  $(".nav-link").click(e => {
    e.stopPropagation();
    e.preventDefault();
    const url = $(e.target).attr("href")
    window.location.href = url
  })

  $(function() {
    if ($("#card-bitcoin").length) {
      loadCoinValues (`${api_host}:${api_host_port}/api/finance/BTC-USD`, 'crypto', 'card-bitcoin', 'marketingOverview-bitcoin', formatCurrency, formatPercent)
      // setInterval(() => {
      //   loadCoinValues (`${api_host}:${api_host_port}/api/finance/BTC-USD`, 'crypto', 'card-bitcoin', 'marketingOverview-bitcoin', formatCurrency, formatPercent)        
      // }, 60000)
    }

    if ($("#card-ethereum").length) {
      loadCoinValues (`${api_host}:${api_host_port}/api/finance/ETH-USD`, 'crypto', 'card-ethereum', 'marketingOverview-ethereum', formatCurrency, formatPercent)
      // setInterval(() => {
      //   loadCoinValues (`${api_host}:${api_host_port}/api/finance/ETH-USD`, 'crypto', 'card-ethereum', 'marketingOverview-ethereum', formatCurrency, formatPercent)
      // }, 60000)
    }

    if ($("#card-solana").length) {
      loadCoinValues (`${api_host}:${api_host_port}/api/finance/SOL-USD`, 'crypto', 'card-solana', 'marketingOverview-solana', formatCurrency, formatPercent)
      // setInterval(() => {
      //   loadCoinValues (`${api_host}:${api_host_port}/api/finance/SOL-USD`, 'crypto', 'card-solana', 'marketingOverview-solana', formatCurrency, formatPercent)
      // }, 60000)
    }    

    if ($("#card-dollar").length) {
      loadCoinValues (`${api_host}:${api_host_port}/api/finance/USD`, 'coin', 'card-dollar', 'marketingOverview-dollar', formatCurrency, formatPercent)
      // setInterval(() => {
      //   loadCoinValues (`${api_host}:${api_host_port}/api/finance/USD`, 'coin', 'card-dollar', 'marketingOverview-dollar', formatCurrency, formatPercent)
      // }, 60000)
    }    

    if ($("#card-euro").length) {
      loadCoinValues (`${api_host}:${api_host_port}/api/finance/EUR`, 'coin', 'card-euro', 'marketingOverview-euro', formatCurrency, formatPercent)
      // setInterval(() => {
      //   loadCoinValues (`${api_host}:${api_host_port}/api/finance/EUR`, 'coin', 'card-euro', 'marketingOverview-euro', formatCurrency, formatPercent)
      // }, 60000)
    }

    if ($("#card-canadianDollar").length) {
      loadCoinValues (`${api_host}:${api_host_port}/api/finance/CAD`, 'coin', 'card-canadianDollar', 'marketingOverview-canadianDollar', formatCurrency, formatPercent)
      // setInterval(() => {
      //   loadCoinValues (`${api_host}:${api_host_port}/api/finance/CAD`, 'coin', 'card-canadianDollar', 'marketingOverview-canadianDollar', formatCurrency, formatPercent)
      // }, 60000)
    }  
    
    if ($("#card-news").length) {
      loadNewsValues()      
    } 
    
    if ($("#card-apis").length) {
      loadListAPIs()
    }
  });
})(jQuery);
