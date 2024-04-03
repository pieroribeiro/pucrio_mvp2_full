const interceptor_service_host = process.env["APP_INTERCEPTOR_HOST"]
const interceptor_service_port = process.env["APP_INTERCEPTOR_PORT"]

module.exports = {
    API: {
        FINANCIAL: {
            AVAILABLE_COINS: ["USD", "EUR", "CAD", "BTC-USD", "ETH-USD", "SOL-USD"],
            API_KEY: "",
            API_URL: `http://${interceptor_service_host}:${interceptor_service_port}/cotacoes`
        },
        NEWS: {
            API_KEY: "",
            API_URL: `http://${interceptor_service_host}:${interceptor_service_port}/news`            
        },
        APIS: {
            API_KEY: "",
            API_URL: `http://${interceptor_service_host}:${interceptor_service_port}/api`
        }
    }
}