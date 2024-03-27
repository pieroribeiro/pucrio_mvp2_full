module.exports = (o) => {
    return {
        title: o.title || '',
        url: o.url || '',
        media: o.source.name || '',
        published_at: o.publishedAt.replace('Z', '') || ''
    }
}
