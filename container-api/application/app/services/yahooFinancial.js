const config = require("../config")
const makeEndpointYahoo = require("../utils/makeEndpointYahoo")

module.exports = (coin) => {
    return new Promise((resolve, reject) => {
        fetch(makeEndpointYahoo(coin))
            .then(res => res.json())
            .then(res => {
                if (res && res["chart"] && res["chart"]["result"] && res["chart"]["result"][0] && res["chart"]["result"][0]["meta"]) {
                    resolve(res["chart"]["result"][0]["meta"])
                } else {
                    resolve([])
                }
            })
            .catch(e => {
                console.log(`ERROR FETCH YAHOO FINANCIAL API: ${e.message}`)
                reject([])
            })
    })
}