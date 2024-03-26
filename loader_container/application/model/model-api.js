module.exports = (o) => {
    return {
        name: o.name || '',
        symbol: o.symbol || '',
        url: o.url || '',
        api_key: o.api_key || '',
        load_symbols: o.load_symbols || ''
    }
}