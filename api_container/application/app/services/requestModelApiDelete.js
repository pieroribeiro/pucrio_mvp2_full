const Fetch = require("../utils/Fetch")
const config = require("../config")

module.exports = (id) => {
    return new Promise((resolve, reject) => {
        Fetch(`${config.API.APIS.API_URL}/${id}`, {headers:{'accept': 'application/json'}})
            .then(res => res.json())
            .then(res => {
                if(res && res.results){
                    return resolve({id: res.results.id, status: 'OK'})
                }
                
                return resolve({id: 0, status: `ITEM_NOT_FOUND`})
            })
            .catch(e => {
                reject({id: 0, status: e.message})
            })
    })
}