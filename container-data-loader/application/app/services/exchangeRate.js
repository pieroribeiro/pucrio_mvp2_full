const makeEndpoint = require("../utils/makeEndpoint-ExchangeRate")

module.exports = (coin) => {
    return new Promise((resolve, reject) => {
        fetch(makeEndpoint(coin, 'BRL'), {headers:{'accept': 'application/json'}})
            .then(res => res.json())
            .then(res => resolve(res))
            .catch(e => {
                console.log(`ERROR FETCH EXCHANGE RATE API: ${e.message}`)
                reject([])
            })
    })
}