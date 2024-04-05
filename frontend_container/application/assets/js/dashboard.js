const api_host = "http://localhost"
const api_host_port = "3002"

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

function writeIncrement (container, value) {
  if (value > 0) {
    $(`${container} .marketingOverview-value-increment`).removeClass("text-danger").addClass('text-success')
  } else if (value < 0) {
    $(`${container} .marketingOverview-value-increment`).removeClass("text-success").addClass('text-danger')
  } else {
    $(`${container} .marketingOverview-value-increment`).removeClass("text-success").removeClass('text-danger')
  }  
}

function loadCoinValues (endpoint, formatValueFN, formatIncrementFN) {
  fetch(endpoint, {headers: {"accept": "application/json", "Content-type": "application/json"}})
    .then(res => res.json())
    .then(res => {
      if (res && res.results && res.results.length > 0) {
        const data = res.results.map(item => parseFloat(item.value))
        const graphData = res.results.map(item => {return {x: item.created_at, y: parseFloat(item.value)}})
        const container = $("#graphics")
        
        const containerID = res.results[0]["symbol"]
        const containerName = res.results[0]["name"]
        const incrementValue = (parseFloat(res.results[res.results.length - 1]["variation"]) / 100)
        // console.log(`incrementValue: ${formatIncrementFN(incrementValue / 100)}`)

        container.append(`
          <div class="col-6 grid-margin stretch-card">
            <div class="card card-rounded">
              <div id="card-${containerID}" class="card-body">
                <div class="d-sm-flex justify-content-between align-items-start">
                  <h4 class="card-title card-title-dash">Market Overview: ${containerName}</h4>
                </div>
                <div class="d-sm-flex align-items-center mt-1 justify-content-between">
                  <div class="d-sm-flex align-items-center mt-4 justify-content-between">
                    <h2 class="me-2 fw-bold marketingOverview-value">${ formatValueFN('pt-BR', 'BRL', data[data.length - 1]) }</h2>
                    <h4 class="me-2">BRL</h4>
                    <h4 class="marketingOverview-value-increment">${(incrementValue === 0.00) ? `` : `(${formatIncrementFN(incrementValue)})`}</h4>
                  </div>
                </div>
                <div class="chartjs-bar-wrapper mt-3">
                  <canvas id="marketingOverview-${containerID}"></canvas>
                </div>
              </div>
            </div>
          </div>
        `)
        writeIncrement (`#card-${containerID}`, incrementValue)
        
        loadGraph(`marketingOverview-${containerID}`, graphData)
      }
    })
    .catch(e => {
      console.error('Erro ao carregar dados financeiros.', `Message: ${e.message}`, e)
    })
}

function loadNewsValues () {
  fetch(`${api_host}:${api_host_port}/news`, {headers: {"accept": "application/json", "Content-type": "application/json"}})
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

function listAPIsActions () {
  $(document).on('click', 'button[data-action="edit-record"]', (e) => {
    e.stopPropagation();
    e.preventDefault();
    const data = e.target.dataset

    fetch(`${api_host}:${api_host_port}/api/${data["id"]}`, {method: 'GET', headers: {"accept": "application/json", "Content-type": "application/json"}})
      .then(res => res.json())
      .then(res => {
        if (res && res.status === 'OK') {              
          $("#modal-admin .modal-body").empty()

          $("#modal-admin .modal-body").append(`
            <form class="formEditApi">
              <input type="hidden" name="id" value="${res.results["id"]}">
              <div class="form-group">
                <label for="api_name">Nome da API</label>
                <input type="text" class="form-control" id="api_name" name="name" placeholder="Nome da API" value="${res.results["name"]}">
              </div>
              <div class="form-group">
                <label for="api_symbol">Símbolo</label>
                <input type="text" class="form-control" id="api_symbol" name="symbol" placeholder="Nome da API" value="${res.results["symbol"]}">
              </div>
              <div class="form-group">
                <label for="api_url">API URL</label>
                <input type="text" class="form-control" id="api_url" name="url" placeholder="URL da API" value="${res.results["url"]}">
              </div>
              <div class="form-group">
                <label for="api_key">API Key</label>
                <input type="text" class="form-control" id="api_key" name="api_key" placeholder="API Key" value="${res.results["api_key"]}">
              </div>
              <div class="form-group">
                <label for="api_load_symbols">Símbolos da API</label>
                <input type="text" class="form-control" id="api_load_symbols" name="load_symbols" placeholder="Símbolos da API" value="${res.results["load_symbols"]}">
              </div>
              <div class="form-group">
                <label for="api_active">Status</label>
                <select class="form-control" id="api_active" name="active">
                  <option value="1" ${(res.results["active"] === 1) ? 'selected' : ''}>Ativo</option>
                  <option value="0" ${(res.results["active"] === 0) ? 'selected' : ''}>Inativo</option>
                </select>
              </div>
            </form>
          `)
          
          $("#modal-admin").modal("show")
        } else {
          showAlert(`A Api ${data["name"]} não encontrada.`, 'warning')
        }
      })
      .catch(e => {
        showAlert(`A Api ${data["name"]} não encontrada para ser excluída.`, 'danger')
      })
  })

  $(document).on('click', 'button[data-action="delete-record"]', (e) => {
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

  $(document).on('click', 'button[data-action="close-modal"]', (e) => {
    e.stopPropagation();
    e.preventDefault();
    $("#modal-admin").modal("hide")
  })

  $(document).on('click', '#modal-admin button[data-action="save-record"]', (e) => {
    e.stopPropagation()
    e.preventDefault()
    
    const data = objectifyForm($("#modal-admin .formEditApi").serializeArray())
    fetch(`${api_host}:${api_host_port}/api/${data["id"]}`, {method: 'PUT', body: JSON.stringify(data), headers: {"accept": "application/json", "Content-type": "application/json"}})
    .then(res => res.json())
    .then(res => {
      if (res && res.status && res.status === 'OK') {
        $('button[data-action="close-modal"]').click()
        showAlert(`Os dados foram atualizados com sucesso.`, 'success')
        loadListAPIs()
      } else {
        $('button[data-action="close-modal"]').click()
        showAlert(`Os dados não foram atualizados. Por favor, tente novamente mais tarde.`, 'warning')
        loadListAPIs()
      }
    })
    .catch(e => {
      $('button[data-action="close-modal"]').click()
      showAlert(`Os dados não podem ser alterados neste momento. Tente novamente mais tarde. Erro: ${e.message}`, 'danger')
      loadListAPIs()
    })
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
                <button type="button" class="btn btn-warning" data-action="edit-record" data-id="${item.id}" data-name="${item.name}" data-toggle="modal" data-target="#modal-admin">Editar</button>
                <button type="button" class="btn btn-danger" data-action="delete-record" data-id="${item.id}" data-name="${item.name}">Excluir</button>
              </div>
            </div>
          </div>
        </li>
        `)
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
    if ($("#graphics").length) {
      loadCoinValues (`${api_host}:${api_host_port}/finance/BTC`, formatCurrency, formatPercent)
      loadCoinValues (`${api_host}:${api_host_port}/finance/ETH`, formatCurrency, formatPercent)
      loadCoinValues (`${api_host}:${api_host_port}/finance/ARS`, formatCurrency, formatPercent)
      loadCoinValues (`${api_host}:${api_host_port}/finance/USD`, formatCurrency, formatPercent)
      loadCoinValues (`${api_host}:${api_host_port}/finance/EUR`, formatCurrency, formatPercent)
      loadCoinValues (`${api_host}:${api_host_port}/finance/CAD`, formatCurrency, formatPercent)
      loadCoinValues (`${api_host}:${api_host_port}/finance/GBP`, formatCurrency, formatPercent)
    }
    
    if ($("#card-news").length) {
      loadNewsValues()      
    } 
    
    if ($("#card-apis").length) {
      loadListAPIs()

      listAPIsActions()
    }
  });
})(jQuery);
