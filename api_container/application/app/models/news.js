module.exports = (o) => {
    return {
        title: o.title || '',
        media: o.media || '',
        url: o.url || '',
        published_at: o.published_at || new Date()
    }
}
