const Fetch = require("../utils/Fetch")
const config = require("../config")
const model = require("../models/api")

module.exports = (coin) => {
    return new Promise((resolve, reject) => {
        Fetch(`${config.API.APIS.API_URL}`, {headers:{'accept': 'application/json'}})
            .then(res => res.json())
            .then(res => {
                if(res && res.results){
                    return resolve({results: res.results.map(item => model(item))})
                }
                
                return resolve({results: []})
            })
            .catch(e => {
                reject([])
            })
    })
}