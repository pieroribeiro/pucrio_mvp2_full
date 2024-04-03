module.exports = (endpoint, coin) => {
    const interceptorServiceHostname = process.env.APP_INTERCEPTOR_HOST || "host"
    const interceptorServicePort = process.env.APP_INTERCEPTOR_PORT || 3000
    const reqParams = {
        method: 'POST',
        body: JSON.stringify(coin),
        headers:{
            'accept': 'application/json',
            'Content-type': 'application/json'
        }
    }
    return fetch(`http://${interceptorServiceHostname}:${interceptorServicePort}${endpoint}`, reqParams)
}