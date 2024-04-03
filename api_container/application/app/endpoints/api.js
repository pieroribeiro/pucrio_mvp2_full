const routes = require('express').Router({ mergeParams: true })

const requestInterceptorApi = require("../services/requestInterceptorApi")

routes.get("/:id([0-9]+)?", async (req, res) => {
    try {
        const id = req.params.id && req.params.id != '' ? req.params.id : null
        const APIResponse = await requestInterceptorApi.get(id)
        let statusCode = 404
        if (APIResponse && APIResponse["results"]) {
            statusCode = 200
        }

        return res.status(statusCode).json(APIResponse)
    } catch (e) {
        console.log(`[ERROR - LOAD INTERCEPTOR API DATA]: ${e.message}`)
        return res.status(500).json({results: [], status: 'ERROR', message: e.message})
    }
})

routes.delete("/:id([0-9]+)", async (req, res) => {
    try {
        const APIResponse = await requestInterceptorApi.remove(req.params.id)
        let statusCode = 404
        if (APIResponse && APIResponse["id"] && APIResponse["id"] > 0) {
            statusCode = 200
        }

        return res.status(statusCode).json(APIResponse)
    } catch (e) {
        console.log(`[ERROR - LOAD INTERCEPTOR API DATA]: ${e.message}`)
        return res.status(500).json({id: -1, status: 'ERROR', message: e.message})
    }
})

routes.put("/:id([0-9]+)", async (req, res) => {
    try {
        const APIResponse = await requestInterceptorApi.update(req.params.id, req.body)
        let statusCode = 500
        if (APIResponse && APIResponse["id"] && APIResponse["id"] > 0) {
            statusCode = 200
        }

        return res.status(statusCode).json(APIResponse)
    } catch (e) {
        console.log(`[ERROR - LOAD INTERCEPTOR API DATA]: ${e.message}`, e)
        return res.status(500).json({id: -1, status: 'ERROR', message: e.message})
    }
})

module.exports = routes
