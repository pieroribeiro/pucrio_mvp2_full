const config = require("../config")

module.exports = (coin) => {
    return config.API.YAHOO.FINANCIAL.ENDPOINT.replace('[COIN]', coin)
}