// scripts.js

// Load Google Charts API
google.charts.load('current', {'packages':['corechart'], 'language': 'pt-BR'});
google.charts.setOnLoadCallback(drawCharts);

const EXCHANGE_RATE_API_KEY = "2130d4fcfb2c8196725dea41"
const EXCHANGE_RATE_API = `https://v6.exchangerate-api.com/v6/${EXCHANGE_RATE_API_KEY}/pair`
const BLOCKCHAIN_API = `https://api.blockchain.com/v3/exchange/tickers`

const Fetch = (url, objRequest) => fetch(url, objRequest).catch(e => console.log(e))
const makeExchangeRateAPIURL = (symbolFrom, symbolTo) => `${EXCHANGE_RATE_API}/${symbolFrom}/${symbolTo}`
const makeBlockchainAPIURL = (symbol) => `${BLOCKCHAIN_API}/${symbol}`

// Function to draw Google Charts
function drawCharts() {
    const symbols = {
        coins: [
            {
                symbol:"USD",
                name:"United States Dollar"
            },
            {
                symbol: "EUR",
                name: "Euro"
            },
            {
                symbol: "CAD",
                name: "Canadian Dollar"
            }
        ],
        cryptos: [
            {
                symbol:"BTC-USD",
                name:"Bitcoin"
            },
            {
                symbol:"ETH-USD",
                name:"Ethereum"
            },
            {
                symbol:"SOL-USD",
                name:"Solana"
            }
        ]
    }

    Fetch(makeExchangeRateAPIURL(symbols.coins[0].symbol, 'BRL'), {headers:{'accept': 'application/json'}}).then(res=>res.json()).then(res => {
        const dollarValue = res.conversion_rate
        drawChart(`chart_coin_${symbols.coins[0].symbol}`, [['Moeda', 'Valor'], [symbols.coins[0].name, dollarValue]]);

        Fetch(makeExchangeRateAPIURL(symbols.coins[1].symbol, 'BRL'), {headers:{'accept': 'application/json'}}).then(res=>res.json()).then(res => {
            drawChart(`chart_coin_${symbols.coins[1].symbol}`, [['Moeda', 'Valor'], [symbols.coins[1].name, res.conversion_rate]]);
        })

        Fetch(makeExchangeRateAPIURL(symbols.coins[2].symbol, 'BRL'), {headers:{'accept': 'application/json'}}).then(res=>res.json()).then(res => {
            drawChart(`chart_coin_${symbols.coins[2].symbol}`, [['Moeda', 'Valor'], [symbols.coins[2].name, res.conversion_rate]]);
        })

        Fetch(makeBlockchainAPIURL(symbols.cryptos[0].symbol), {headers:{'accept': 'application/json'}}).then(res=>res.json()).then(res => {
            drawChart(`chart_crypto_${symbols.cryptos[0].symbol}`, [['Moeda', 'Valor'], [symbols.cryptos[0].name, (res.last_trade_price * dollarValue)]]);
        })

        Fetch(makeBlockchainAPIURL(symbols.cryptos[1].symbol), {headers:{'accept': 'application/json'}}).then(res=>res.json()).then(res => {
            drawChart(`chart_crypto_${symbols.cryptos[1].symbol}`, [['Moeda', 'Valor'], [symbols.cryptos[1].name, (res.last_trade_price * dollarValue)]]);
        })

        Fetch(makeBlockchainAPIURL(symbols.cryptos[2].symbol), {headers:{'accept': 'application/json'}}).then(res=>res.json()).then(res => {
            drawChart(`chart_crypto_${symbols.cryptos[2].symbol}`, [['Moeda', 'Valor'], [symbols.cryptos[2].name, (res.last_trade_price * dollarValue)]]);
        })
    })
}

// Function to draw Google Chart
function drawChart(elementId, data) {
    var chartData = google.visualization.arrayToDataTable(data);

    var options = {
        title: data[0][0] + ' em BRL',
        curveType: 'function',
        legend: { position: 'bottom' },
        vAxis: {
            format: 'currency'
        }
    };

    var chart = new google.visualization.LineChart(document.getElementById(elementId));
    chart.draw(chartData, options);
}
