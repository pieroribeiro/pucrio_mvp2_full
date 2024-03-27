const schedule = require('node-schedule');
const { exec } = require('child_process');

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

schedule.scheduleJob('*/5 * * * *', () => executarScript('load-coin.js'));
schedule.scheduleJob('*/5 * * * *', () => executarScript('load-crypto.js'));
schedule.scheduleJob('*/5 * * * *', () => executarScript('load-news.js'));