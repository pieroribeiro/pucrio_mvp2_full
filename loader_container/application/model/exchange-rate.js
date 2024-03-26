module.exports = (o) => {
    return {
        symbol: o.base_code || '',
        name: o.name || '',
        type: o.type || '',
        value: o.conversion_rate || ''
    }
}