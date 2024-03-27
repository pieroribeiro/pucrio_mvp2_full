const requestModelNews = require("../services/requestModelNews")

module.exports = async (req, res) => {
    try {
        const news = await requestModelNews()
        if (news) {
            res.status(200).json(news)
        } else {
            res.status(404).json({status: 'DATA_NOT_FOUND'})
        }
    } catch (e) {
        console.log(`[ERROR - LOAD MODEL NEWS DATA]: ${e.message}`)
        res.status(500).json({status: 'ERROR', message: e.message})
    }
}