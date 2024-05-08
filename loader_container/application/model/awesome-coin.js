module.exports = (o) => {
    return {
        symbol: o.code || '',
        name: o.name || '',
        type: o.type || '',
        variation: parseFloat(o.pctChange || 0),
        value_buy: parseFloat(o.bid || 0),
        value_sell: parseFloat(o.ask || 0)
    }
}