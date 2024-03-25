const makeEndpoint = require("../utils/makeEndpoint-Blockchain")

module.exports = (coin) => {
    return new Promise((resolve, reject) => {
        fetch(makeEndpoint(coin), {headers:{'accept': 'application/json'}})
            .then(res => res.json())
            .then(res => resolve(res))
            .catch(e => {
                console.log(`ERROR FETCH EXCHANGE RATE API: ${e.message}`)
                reject([])
            })
    })
}