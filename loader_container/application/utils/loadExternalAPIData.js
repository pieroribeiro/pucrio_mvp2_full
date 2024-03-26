module.exports = (api, params) => {
    return fetch(api, params).then(res => res.json())
}