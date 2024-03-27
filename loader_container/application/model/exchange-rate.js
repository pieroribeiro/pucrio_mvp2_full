module.exports = (o) => {
    return {
        symbol: o.base_code || '',
        name: o.name || '',
        value: o.conversion_rate || '',
        type: 'coin'
    }
}
