const getCoin = require("../utils/getCoinExchangeRate")
const sendToModelService = require("../services/sendToModelService")
const apiRequest = require("../services/exchangeRate")

module.exports = async (req, res) => {
    try {
        const coin = getCoin(req.params.coin)
        if (coin) {
            const apiResults = await apiRequest(coin)
            if (apiResults) {
                await sendToModelService(apiResults)
                res.status(200).json({status: 'OK'})
            } else {
                res.status(404).json({status: 'DATA_NOT_FOUND'})
            }
        } else {
            res.status(404).json({status: 'COIN_NOT_FOUND'})
        }
    } catch (e) {
        console.log(`[ERROR - LOAD EXCHANGE RATE FINANCIAL]: ${e.message}`)
        res.status(500).json({status: 'ERROR', message: e.message})
    }
}