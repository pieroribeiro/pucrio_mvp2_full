USE mvp2;

CREATE TABLE IF NOT EXISTS `apis` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL,
    `symbol` VARCHAR(100) NOT NULL,
    `url` VARCHAR(500) NOT NULL,
    `api_key` VARCHAR(200) NOT NULL,
    `load_symbols` VARCHAR(300) NOT NULL,
    `active` TINYINT(1) NOT NULL DEFAULT 1,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (symbol)
);

CREATE TABLE IF NOT EXISTS `cotacoes` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `symbol` VARCHAR(10) NOT NULL,
    `name` VARCHAR(100) NOT NULL,
    `value` DECIMAL(10, 2) NOT NULL,
    `type` VARCHAR(20) NOT NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS `news` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `title` VARCHAR(300) NOT NULL,
    `url` VARCHAR(500) NOT NULL,
    `media` VARCHAR(500) NOT NULL,
    `published_at` TIMESTAMP NOT NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

/*
INSERT INTO apis (`name`, `symbol`, `url`, `api_key`, `load_symbols`, `active`) VALUES ('Exchange Rate API', 'coin', 'https://v6.exchangerate-api.com/v6/pair', '2130d4fcfb2c8196725dea41', 'USD|Dollar,EUR|Euro,CAD|Canadian Dollar', 1);
INSERT INTO apis (`name`, `symbol`, `url`, `api_key`, `load_symbols`, `active`) VALUES ('Blockchain API', 'crypto', 'https://api.blockchain.com/v3/exchange/tickers', '', 'BTC-USD|Bitcoin,ETH-USD|Ethereum,SOL-USD|Solana', 1);
*/

INSERT INTO apis (`name`, `symbol`, `url`, `api_key`, `load_symbols`, `active`) VALUES ('News API', 'news', 'https://newsapi.org/v2/top-headlines', '47a44c3467c84467a0ccd7ae0db9ad9b', 'country=br&category=business&pageSize=10', 1);
INSERT INTO apis (`name`, `symbol`, `url`, `api_key`, `load_symbols`, `active`) VALUES ('Awesome API', 'coin', 'https://economia.awesomeapi.com.br/json/last', '', 'BTC-BRL|crypto,ETH-BRL|crypto,ARS-BRL|coin,USD-BRL|coin,EUR-BRL|coin,CAD-BRL|coin', 1);
