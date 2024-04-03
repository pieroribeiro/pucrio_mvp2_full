const requestInterceptorNews = require("../services/requestInterceptorNews")

module.exports = async (req, res) => {
    try {
        const news = await requestInterceptorNews()
        if (news) {
            res.status(200).json(news)
        } else {
            res.status(404).json({status: 'DATA_NOT_FOUND'})
        }
    } catch (e) {
        console.log(`[ERROR - LOAD INTERCEPTOR NEWS DATA]: ${e.message}`)
        res.status(500).json({status: 'ERROR', message: e.message})
    }
}