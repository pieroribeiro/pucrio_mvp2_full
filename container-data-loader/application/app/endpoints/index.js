const getCoin = require("../utils/getCoin")
const sendToModelService = require("../services/sendToModelService")
const yahooFinancial = require("../services/yahooFinancial")

module.exports = async (req, res) => {
    try {
        const coin = getCoin(req.params.coin)
        const yahooAPI = await yahooFinancial(coin)
        if (yahooAPI) {
            await sendToModelService(coin)
            res.status(200).json({status: 'OK'})
        } else {
            res.status(404).json({status: 'COIN_OR_DATA_NOT_FOUND'})
        }

        res.status(200).json({status: 'ok'})
    } catch (e) {
        console.log(`[ERROR - LOAD FINANCIAL]: ${e.message}`)
        res.status(500).json({status: 'ERROR', message: e.message})
    }
}