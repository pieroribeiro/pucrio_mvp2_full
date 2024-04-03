const getAPIFromDB = require("./utils/getAPIsFromDB")
const loadExternalAPIData = require("./utils/loadExternalAPIData")
const saveService = require("./utils/saveService")
const modelApi = require("./model/model-api")
const model = require("./model/exchange-rate")
const endpoint = "/api/coin"


/*{'status': 'CREATED', 'id': recordId}*/
const init = (apiEndpoint) => {
    getAPIFromDB(apiEndpoint)
    .then(res => res.json())
    .then(resApi => {              
        if (resApi && resApi.results && resApi.results.id) {
            const apiData = modelApi(resApi.results)
            apiParams = {
                headers: {
                    'accept': 'application/json',
                    'Content-type': 'application/json',
                    'Cache-control': 'no-cache, no-store'
                }
            }

            if (apiData.api_key.length > 0) {
                apiParams.headers["Authorization"] = `Bearer ${apiData.api_key}`
            }

            if (apiData.load_symbols.length > 0) {
                apiData.load_symbols.split(',').forEach(sym => {
                    const coin = sym.split("|")
                    const coinSymbol = coin[0] || ''
                    const coinName = coin[1] || ''

                    loadExternalAPIData(`${apiData.url}/${coinSymbol}/BRL`, apiParams)
                    .then(res => res.json())
                    .then(resExternalAPI => {
                        if (resExternalAPI.result === "success") {
                            resExternalAPI.name = coinName
                            saveService('/cotacoes', model(resExternalAPI))
                            .then(res => res.json())
                            .then(resSave => {
                                if (resSave && resSave.status == 'CREATED') {
                                    console.log(`SAVE-COIN: Dados salvos com sucesso. Coin ${resSave.id}`, resSave)
                                } else {
                                    console.log(`SAVE-COIN: [ERROR] Ocorreu um erro`, resSave)
                                }
                            }).catch(e => {
                                console.log(`SAVE-COIN: [ERROR] Erro ao salvar dados da API Externa (/${coinSymbol}/BRL) no Banco de Dados: ${apiData.url}. Message: ${e.message}`)
                            })
                        } else {
                            console.log(`SAVE-COIN: [ERROR] Erro ao retornar dados da API Externa (/${coinSymbol}/BRL): ${apiData.url}. Message: ${resExternalAPI["error-type"]}`)
                        }
                    }).catch(e => {
                        console.log(`LOAD-COIN: [ERROR] Erro ao carregar dados da API Externa (/${coinSymbol}/BRL): ${apiData.url}. Message: ${e.message}`)
                    })
                })
            }
        } else {
            console.log("LOAD-COIN: [ERROR] API não encontrada")
        }
    }).catch(e => {
        console.log(`LOAD-COIN: [ERROR] Erro ao carregar dados da API INTERCEPTOR (${apiEndpoint}): Message: ${e.message}`, e)    
    })
}

init(endpoint)