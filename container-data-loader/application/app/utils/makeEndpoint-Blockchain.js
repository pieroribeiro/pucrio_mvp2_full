const config = require("../config")

module.exports = (symbol) => `${config.API.BLOCKCHAIN.API_URL}/${symbol}`
