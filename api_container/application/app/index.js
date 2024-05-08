const express = require('express')
const app = express()
app.use(express.json())
const helmet = require('helmet')
app.use(helmet())
const cors = require('cors')
app.use(cors())

const fs = require("fs")
const YAML = require('yaml')
const swaggerUi = require('swagger-ui-express')
const swaggerConfigFile = fs.readFileSync('./swagger.yaml', 'utf8')
const swaggerDocument = YAML.parse(swaggerConfigFile)

const middleware = (req, res, next) => {
    res.header("Access-Control-Allow-Origin", "*")
    res.header("Access-Control-Allow-Methods", "*")
    res.header("Access-Control-Allow-Headers", "*")

    next()
}

app.use('/', middleware, require('./router'))
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument))

module.exports = app
