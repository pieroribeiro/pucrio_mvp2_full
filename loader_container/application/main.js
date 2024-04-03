const schedule = require('node-schedule');
const { exec } = require('child_process');
const timeToExecuteCoin = process.env["TIME_TO_EXEC_COIN"]
// const timeToExecuteCrypto = process.env["TIME_TO_EXEC_CRYPTO"]
const timeToExecuteNews = process.env["TIME_TO_EXEC_NEWS"]

const executarScript = (scriptName) => {
    exec(`node ${scriptName}`, (error, stdout, stderr) => {
        if (error) {
            console.log(`Erro: ${error}`);
            return;
        }
        console.log(stdout);
        if (stderr) {
            console.log(`Erro de execução: ${stderr}`);
        }
    });    
}

schedule.scheduleJob(timeToExecuteCoin, () => executarScript('load-coin.js'));
// schedule.scheduleJob(timeToExecuteCrypto, () => executarScript('load-crypto.js'));
schedule.scheduleJob(timeToExecuteNews, () => executarScript('load-news.js'))