module.exports = (o) => {
    return {
        symbol: o.symbol || '',
        name: o.name || '',
        type: 'crypto',
        value: o.last_trade_price || ''
    }
}