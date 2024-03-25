const routes = require('express').Router({ mergeParams: true })

routes.get('/health', require("../endpoints/health"))
routes.get('/load/financial/coin/:coin([a-zA-Z0-9-]{3,10})', require("../endpoints/coin.js"))
routes.get('/load/financial/crypto/:crypto([a-zA-Z0-9-]{3,10})', require("../endpoints/crypto.js"))

module.exports = routes
