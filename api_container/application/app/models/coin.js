module.exports = (o) => {
    return {
        name: o.name || '',
        symbol: o.symbol || '',
        value_buy: o.value_buy || 0,
        value_sell: o.value_sell || 0,
        variation: o.variation || 0,
        created_at: o.created_at || new Date()
    }
}
