module.exports = (o) => {
    return {
        name: o.name || '',
        symbol: o.symbol || '',
        value: o.value || 0,
        variation: o.variation || 0,
        created_at: o.created_at || new Date()
    }
}
