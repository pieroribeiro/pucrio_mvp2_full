const requestInterceptorFinance = require("../services/requestInterceptorFinance")

module.exports = async (req, res) => {
    try {
        const coinValues = await requestInterceptorFinance(req.params.coin)
        if (coinValues) {
            res.status(200).json(coinValues)
        } else {
            res.status(404).json({status: 'DATA_NOT_FOUND'})
        }
    } catch (e) {
        console.log(`[ERROR - LOAD INTERCEPTOR FINANCIAL DATA]: ${e.message}`)
        res.status(500).json({status: 'ERROR', message: e.message})
    }
}