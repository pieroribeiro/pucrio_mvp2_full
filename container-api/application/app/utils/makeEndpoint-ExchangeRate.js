const config = require("../config")

module.exports = (symbolFrom, symbolTo) => `${config.API.EXCHANGE_RATE.API_URL}/${config.API.EXCHANGE_RATE.API_KEY}/pair/${symbolFrom}/${symbolTo}`
