const getAPIFromDB = require("./utils/getAPIsFromDB")
const loadExternalAPIData = require("./utils/loadExternalAPIData")
const saveService = require("./utils/saveService")
const modelApi = require("./model/model-api")
const model = require("./model/blockchain")
const endpoint = "/api/crypto"

const init = (apiEndpoint) => {
    getAPIFromDB(apiEndpoint)
    .then(res => res.json())
    .then(resAPI => {        
        if (resAPI && resAPI.result && resAPI.result.id) {
            const apiData = modelApi(resAPI.result)
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

                    loadExternalAPIData(`${apiData.url}/${coinSymbol}`, apiParams)
                    .then(res => res.json())
                    .then(resExternalAPI => {
                        resExternalAPI.name = coinName
                        saveService('/cotacoes', model(resExternalAPI))
                        .then(res => res.json())
                        .then(resSave => {
                            if (resSave && resSave.status == 'CREATED') {
                                console.log(`SAVE-CRYPTO: Dados salvos com sucesso. Coin ${resSave.id}`, resSave)
                            } else {
                                console.log(`SAVE-CRYPTO: [ERROR] Ocorreu um erro`, resSave)                                
                            }
                        }).catch(e => {
                            console.log(`SAVE-CRYPTO: [ERROR] Erro ao salvar dados da API Externa (/${coinSymbol}/BRL) no Banco de Dados: ${apiData.url}. Message: ${e.message}`)
                        })
                    }).catch(e => {
                        console.log(`LOAD-CRYPTO: [ERROR] Erro ao carregar dados da API Externa (/${coinSymbol}): ${apiData.url}. Message: ${e.message}`)
                    })
                })
            }
        } else {
            console.log("LOAD-CRYPTO: [ERROR] API não encontrada")
        }
    }).catch(e => {
        console.log(`LOAD-CRYPTO: [ERROR] Erro ao carregar dados da API Model (${apiEndpoint}): Message: ${e.message}`)
    })
}

init(endpoint)