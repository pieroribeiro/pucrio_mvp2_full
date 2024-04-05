module.exports = (o) => {
    return {
        symbol: o.code || '',
        name: o.name || '',
        type: o.type || '',
        variation: parseFloat(o.pctChange || 0),
        value: parseFloat(o.ask || 0)
    }
}