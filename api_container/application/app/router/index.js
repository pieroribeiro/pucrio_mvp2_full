const routes = require('express').Router({ mergeParams: true })

routes.get('/health', require("../endpoints/health"))
routes.get('/api/finance/:coin([a-zA-Z0-9-]{3,10})', require("../endpoints/coin"))
routes.get('/api/news', require("../endpoints/news"))

module.exports = routes
