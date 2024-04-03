const getAPIFromDB = require("./utils/getAPIsFromDB")
const loadExternalAPIData = require("./utils/loadExternalAPIData")
const saveService = require("./utils/saveService")
const modelApi = require("./model/model-api")
const model = require("./model/news")
const endpoint = "/api/news"

const init = (apiEndpoint) => {
    getAPIFromDB(apiEndpoint)
    .then(res => res.json())
    .then(resAPI => {        
        if (resAPI && resAPI.results && resAPI.results.id) {
            const apiData = modelApi(resAPI.results)
            apiParams = {
                headers: {
                    'accept': 'application/json',
                    'Content-type': 'application/json',
                    'Cache-control': 'no-cache, no-store'
                }
            }

            if (apiData.api_key.length > 0) {
                apiParams.headers["Authorization"] = `${apiData.api_key}`
            }

            loadExternalAPIData(`${apiData.url}?${apiData.load_symbols}`, apiParams)
            .then(res => res.json())
            .then(resExternalAPI => {
                if (resExternalAPI && resExternalAPI.articles.length > 0) {
                    resExternalAPI.articles.forEach(resNotice => {
                        saveService('/news', model(resNotice))
                        .then(res => res.json())
                        .then(resSave => {        
                            if (resSave && resSave.status == 'CREATED') {                    
                                console.log(`SAVE-NEWS: Dados salvos com sucesso. News ${resSave.id}`, resSave)
                            } else {
                                console.log(`SAVE-NEWS: [ERROR] Ocorreu um erro`, resSave) 
                            }
                        }).catch(e => {
                            console.log(`SAVE-NEWS: [ERROR] Erro ao salvar dados da API Externa (News) no Banco de Dados: ${apiData.url}. Message: ${e.message}`)
                        })
                    })
                }
            }).catch(e => {
                console.log(`LOAD-NEWS: [ERROR] Erro ao carregar dados da API Externa (News): ${apiData.url}. Message: ${e.message}`)
            })
        } else {
            console.log("LOAD-NEWS: [ERROR] API não encontrada")
        }
    }).catch(e => {
        console.log(`LOAD-NEWS: [ERROR] Erro ao carregar dados da API INTERCEPTOR (${apiEndpoint}): Message: ${e.message}`)       
    })
}

init(endpoint)