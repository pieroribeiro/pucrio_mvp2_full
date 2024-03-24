const config = require("../config")

module.exports = (coin) => {
    return (config.API.EXCHANGE_RATE.AVAILABLE_COINS.includes(coin)) ? coin : null
}