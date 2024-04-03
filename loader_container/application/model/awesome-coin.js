module.exports = (o) => {
    return {
        symbol: o.code || '',
        name: o.name || '',
        type: o.type || '',
        value: parseFloat(o.high) || 0
    }
}