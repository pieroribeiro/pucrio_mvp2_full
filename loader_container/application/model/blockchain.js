module.exports = (o) => {
    return {
        symbol: o.symbol || '',
        name: o.name || '',
        type: o.type || '',
        value: o.last_trade_price || ''
    }
}