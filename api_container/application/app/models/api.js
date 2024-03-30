module.exports = (o) => {
    return {
        id: o.id || 0,
        name: o.name || '',
        symbol: o.symbol || '',
        url: o.url || 0,
        api_key: o.api_key || 0,
        load_symbols: o.load_symbols || 0,
        active: o.active || 0,
        created_at: o.created_at || new Date()
    }
}
