const getCoin = require("../utils/getCoinBlockchain")
const sendToModelService = require("../services/sendToModelService")
const apiRequest = require("../services/blockchain")

module.exports = async (req, res) => {
    try {
        const coin = getCoin(req.params.crypto)
        if (coin) {
            const apiResults = await apiRequest(coin)
            if (apiResults) {
                await sendToModelService(apiResults)
                res.status(200).json({status: 'OK'})
            } else {
                res.status(404).json({status: 'DATA_NOT_FOUND'})
            }
        } else {
            res.status(404).json({status: 'CRYPTO_NOT_FOUND', data: req.params.crypto})
        }
    } catch (e) {
        console.log(`[ERROR - LOAD BLOCKCHAIN FINANCIAL]: ${e.message}`)
        res.status(500).json({status: 'ERROR', message: e.message})
    }
}