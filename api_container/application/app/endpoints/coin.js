const requestModelFinance = require("../services/requestModelFinance")

module.exports = async (req, res) => {
    try {
        const coinValues = await requestModelFinance(req.params.coin)
        if (coinValues) {
            res.status(200).json(coinValues)
        } else {
            res.status(404).json({status: 'DATA_NOT_FOUND'})
        }
    } catch (e) {
        console.log(`[ERROR - LOAD MODEL FINANCIAL DATA]: ${e.message}`)
        res.status(500).json({status: 'ERROR', message: e.message})
    }
}