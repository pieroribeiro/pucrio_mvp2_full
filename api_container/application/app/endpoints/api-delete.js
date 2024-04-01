const requestModelApiDelete = require("../services/requestModelApiDelete")

module.exports = async (req, res) => {
    try {
        const {status, id} = await requestModelApiDelete(req.params.id)
        if (id && id > 0) {
            res.status(200).json({id, status})
        } else {
            res.status(404).json({id, status})
        }
    } catch (e) {
        console.log(`[ERROR - LOAD MODEL API DATA]: ${e.message}`)
        res.status(500).json({id: -1, status: `ERROR: ${e.message}`})
    }
}