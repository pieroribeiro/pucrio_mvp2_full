const config = require("../config")

module.exports = (coin) => {
    return (config.AVAILABLE_COINS.includes(coin)) ? coin : "XXXXXX"
}