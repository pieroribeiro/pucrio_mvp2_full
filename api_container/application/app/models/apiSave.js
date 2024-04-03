module.exports = (o) => {
    return {
        name: o.name || '',
        symbol: o.symbol || '',
        url: o.url || 0,
        api_key: o.api_key || 0,
        load_symbols: o.load_symbols || 0,
        active: o.active || 0
    }
}
