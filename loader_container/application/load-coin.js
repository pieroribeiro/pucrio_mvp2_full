const getAPIFromDB = require("./utils/getAPIsFromDB")
const loadExternalAPIData = require("./utils/loadExternalAPIData")
const saveService = require("./utils/saveService")
const modelApi = require("./model/model-api")
const model = require("./model/awesome-coin")
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
                const apiParameters = apiData.load_symbols.split(',').map(sym => sym.replace(/\|.*/g, '')).join(',')
                const returnObjects = apiData.load_symbols.split(',').map(sym => sym.replace('-', ''))

                loadExternalAPIData(`${apiData.url}/${apiParameters}`, apiParams)
                .then(res => res.json())
                .then(resExternalAPI => {
                    returnObjects.forEach(item => {
                        const arrCoin = item.split('|')
                        const coinObject = arrCoin[0]
                        resExternalAPI[coinObject].type = arrCoin[1]
                        const coinData = resExternalAPI[coinObject]

                        saveService('/cotacoes', model(coinData))
                        .then(res => res.json())
                        .then(resSave => {
                            if (resSave && resSave.status == 'CREATED') {
                                console.log(`SAVE-COIN: Dados salvos com sucesso. Coin ${resSave.results.id}`, resSave)
                            } else {
                                console.log(`SAVE-COIN: [ERROR] Ocorreu um erro`, resSave)
                            }
                        }).catch(e => {
                            console.log(`SAVE-COIN: [ERROR] Erro ao salvar dados da API Externa (/${coinData.code}) no Banco de Dados: ${apiData.url}. Message: ${e.message}`)
                        })
                    })
                }).catch(e => {
                    console.log(`LOAD-COIN: [ERROR] Erro ao carregar dados da API Externa (${apiData.url}/${apiParameters}). Message: ${e.message}`)
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