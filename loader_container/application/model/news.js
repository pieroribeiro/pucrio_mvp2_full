module.exports = (o) => {
    return {
        title: o.title || '',
        url: (o.url || '').substring(0, 450),
        media: o.source.name || '',
        published_at: o.publishedAt.replace('Z', '') || ''
    }
}
