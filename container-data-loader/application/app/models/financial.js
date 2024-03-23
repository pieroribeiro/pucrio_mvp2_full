module.exports = (o) => {
    return {
        symbol: (o.symbol) ? o.symbol.replace(/[=\-]+/ig, '') : '',
        currency: o.currency || '',
        name: o.name || '',
        regularMarketPrice: o.regularMarketPrice || 0,
        updated_at: o.updated_at || new Date()
    }
}
