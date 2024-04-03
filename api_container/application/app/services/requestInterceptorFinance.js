const Fetch = require("../utils/Fetch")
const config = require("../config")
const model = require("../models/coin")

module.exports = (coin) => {
    return new Promise((resolve, reject) => {
        Fetch(`${config.API.FINANCIAL.API_URL}/${coin}`, {headers:{'accept': 'application/json', 'Content-type': 'application/json'}})
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