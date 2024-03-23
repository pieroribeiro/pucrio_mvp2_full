const routes = require('express').Router({ mergeParams: true })

routes.get('/health', require("../endpoints/health"))
routes.get('/load/financial/:coin', require("../endpoints"))

module.exports = routes
