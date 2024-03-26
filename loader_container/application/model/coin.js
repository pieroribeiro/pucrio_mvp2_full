module.exports = (o) => {
    return {
        symbol: o.symbol || '',
        name: o.name || '',
        type: o.type || '',
        value: o.value || ''
    }
}