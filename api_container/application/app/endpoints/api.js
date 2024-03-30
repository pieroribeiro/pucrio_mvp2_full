const requestModelApi = require("../services/requestModelApi")

module.exports = async (req, res) => {
    try {
        const apiValues = await requestModelApi(req.params.coin)
        if (apiValues) {
            res.status(200).json(apiValues)
        } else {
            res.status(404).json({status: 'DATA_NOT_FOUND'})
        }
    } catch (e) {
        console.log(`[ERROR - LOAD MODEL API DATA]: ${e.message}`)
        res.status(500).json({status: 'ERROR', message: e.message})
    }
}