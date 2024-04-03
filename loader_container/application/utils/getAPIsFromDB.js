module.exports = (enpoint) => {
    const interceptorServiceHostname = process.env.APP_INTERCEPTOR_HOST || "host"
    const interceptorServicePort = process.env.APP_INTERCEPTOR_PORT || 3000
    const reqParams = {
        headers:{
            'accept': 'application/json',
            'Content-type': 'application/json'
        }
    }
    return fetch(`http://${interceptorServiceHostname}:${interceptorServicePort}${enpoint}`, reqParams)
}