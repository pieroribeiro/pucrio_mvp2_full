const Fetch = require("../utils/Fetch")
const config = require("../config")
const model = require("../models/api")

const get = (id) => {
    return new Promise((resolve, reject) => {
        const url = (id && id != '') ? `${config.API.APIS.API_URL}/${id}` : config.API.APIS.API_URL
        Fetch(url, {method: 'GET', headers:{'accept': 'application/json'}})
            .then(res => res.json())
            .then(res => {
                if (res && res.results && res.status) {
                    switch (res.status) {
                        case 'OK':
                            return resolve({results: res.results.map(item => model(item)), status: 'OK', message: null})
                        case 'ERROR':
                            return reject({results: [], status: 'ERROR', message: res.message})
                        default:
                            return resolve({results: [], status: `ITEM_NOT_FOUND`, message: null})
                    }
                } else {
                    return reject({results: [], status: 'ERROR', message: 'An error has occurred'})
                }
            })
            .catch(e => {
                return reject({results: [], status: 'ERROR', message: e.message})
            })
    })
}

const remove = (id) => {
    return new Promise((resolve, reject) => {
        const url = `${config.API.APIS.API_URL}/${id}`
        Fetch(url, {method: 'DELETE', headers:{'accept': 'application/json'}})
            .then(res => res.json())
            .then(res => {
                if (res && res.id && res.status) {
                    switch (res.status) {
                        case 'OK':
                            return resolve({id: res.id, status: 'OK', message: null})
                        case 'ERROR':
                            return reject({id: -1, status: 'ERROR', message: res.message})
                        default:
                            return resolve({id: 0, status: `ITEM_NOT_FOUND`, message: null})
                    }
                } else {
                    return reject({id: -2, status: 'ERROR', message: 'An error has occurred'})
                }
            })
            .catch(e => {
                return reject({id: -3, status: 'ERROR', message: e.message})
            })
    })
}

module.exports = {
    get,
    remove
}