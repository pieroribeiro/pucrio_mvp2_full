module.exports = (endpoint, coin) => {
    const modelServicePort = process.env.APP_MODEL_PORT || 3000
    const modelServiceHostname = process.env.APP_MODEL_HOST || "host"
    console.log(`http://${modelServiceHostname}:${modelServicePort}${endpoint}`)
    const reqParams = {
        method: 'POST',
        body: JSON.stringify(coin),
        headers:{
            'accept': 'application/json',
            'Content-type': 'application/json'
        }
    }
    return fetch(`http://${modelServiceHostname}:${modelServicePort}${endpoint}`, reqParams)
}