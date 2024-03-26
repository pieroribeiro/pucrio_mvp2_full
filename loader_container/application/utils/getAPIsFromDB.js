module.exports = (enpoint) => {
    const modelServicePort = process.env.APP_MODEL_PORT || 3000
    return fetch(`http://localhost:${modelServicePort}${enpoint}`).then(res => res.json())
}