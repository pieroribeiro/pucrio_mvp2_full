const getAPIFromDB = require("./utils/getAPIsFromDB")
const loadExternalAPIData = require("./utils/loadExternalAPIData")
const modelApi = require("./model/model-api")
const model = require("./model/exchange-rate")
const endpoint = "/api/coin"
const coinType = "coin"

const init = (apiEndpoint) => {
    getAPIFromDB(apiEndpoint).then(res => {        
        if (res && res.result && res.result.id) {
            const apiData = modelApi(res.result)
            apiParams = {
                headers: {
                    'accept': 'application/json',
                    'Content-type': 'application/json'
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

                    loadExternalAPIData(`${apiData.url}/${coinSymbol}/BRL`, apiParams).then(resExternalAPI => {
                        resExternalAPI.name = coinName
                        resExternalAPI.type = coinType
                        console.log(`External API Data (/${coinSymbol}/BRL): `, model(resExternalAPI))
                    }).catch(e => {
                        console.log(`LOAD-COIN: [ERROR] Erro ao carregar dados da API Externa (/${coinSymbol}/BRL): ${apiData.url}. Message: ${e.message}`)
                    })
                })
            }
        } else {
            console.log("LOAD-COIN: [ERROR] API não encontrada")
        }
    }).catch(e => {
        console.log(e)        
    })
}

init(endpoint)