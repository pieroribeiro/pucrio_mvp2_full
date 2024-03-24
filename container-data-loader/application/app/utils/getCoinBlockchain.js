const config = require("../config")

module.exports = (coin) => {
    return (config.API.BLOCKCHAIN.AVAILABLE_COINS.includes(coin)) ? coin : null
}