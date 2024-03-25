const express = require('express')
const app = express()
app.use(express.json())
const helmet = require('helmet')
app.use(helmet())

app.use('/', require('./router'))

module.exports = app
