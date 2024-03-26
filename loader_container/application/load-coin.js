const Fetch = require("./utils/Fetch")
const getAPIFromDB = require("./utils/getAPIsFromDB")
const loadExternalAPIData = require("./utils/loadExternalAPIData")
const model = require("./model/coin")
const endpoint = "/api"

const init = () => {
    getAPIFromDB(endpoint).then(res => {
        if (res && res.length > 0) {
            const apiData = res[0]
            apiParams = {}
            if (apiData.api_key.length > 0) {
                apiParams.headers["Authorization"] = `Bearer ${apiData.api_key}`
            }
            loadExternalAPIData(`${apiData.url}/USD/BRL`, apiParams).then(resExternalAPI => {
                console.log("External API Data (/USD/BRL): ", resExternalAPI, model(resExternalAPI))
            }).catch(e => {
                console.log(`LOAD-COIN: [ERROR] Erro ao carregar dados da API Externa (/USD/BRL): ${apiData.url}. Message: ${e.message}`)
            })
            loadExternalAPIData(`${apiData.url}/EUR/BRL`, apiParams).then(resExternalAPI => {
                console.log("External API Data (/EUR/BRL): ", resExternalAPI, model(resExternalAPI))
            }).catch(e => {
                console.log(`LOAD-COIN: [ERROR] Erro ao carregar dados da API Externa (/EUR/BRL): ${apiData.url}. Message: ${e.message}`)
            })
            loadExternalAPIData(`${apiData.url}/CAD/BRL`, apiParams).then(resExternalAPI => {
                console.log("External API Data (/CAD/BRL): ", resExternalAPI, model(resExternalAPI))
            }).catch(e => {
                console.log(`LOAD-COIN: [ERROR] Erro ao carregar dados da API Externa (/CAD/BRL): ${apiData.url}. Message: ${e.message}`)
            })
        } else {
            console.log("LOAD-COIN: [ERROR] API não encontrada")
        }
    }).catch(e => {
        console.log(e)        
    })  
}

init()