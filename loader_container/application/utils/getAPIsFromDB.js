module.exports = (enpoint) => {
    const modelServicePort = process.env.APP_MODEL_PORT || 3000
    const modelServiceHostname = process.env.APP_MODEL_HOST || "host"
    console.log(`http://${modelServiceHostname}:${modelServicePort}${enpoint}`)
    const reqParams = {
        headers:{
            'accept': 'application/json',
            'Content-type': 'application/json'
        }
    }
    return fetch(`http://${modelServiceHostname}:${modelServicePort}${enpoint}`, reqParams).then(res => res.json())
}