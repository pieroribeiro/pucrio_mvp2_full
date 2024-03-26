USE mvp2;

CREATE TABLE IF NOT EXISTS `apis` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL,
    `symbol` VARCHAR(100) NOT NULL,
    `url` VARCHAR(500) NOT NULL,
    `api_key` VARCHAR(100) NOT NULL,
    `active` BIT NOT NULL DEFAULT 1,
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

INSERT INTO apis (`name`, `crypto`, `url`, `api_key`, `active`) VALUES ('Blockchain', 'https://api.blockchain.com/v3/exchange/tickers', '', 1);
INSERT INTO apis (`name`, `coin`, `url`, `api_key`, `active`) VALUES ('Blockchain', 'https://v6.exchangerate-api.com/v6/pair', '2130d4fcfb2c8196725dea41', 1);

INSERT INTO cotacoes (`symbol`, `name`, `value`, `type`) VALUES ('USD', 'Dollar', 5.03, 'coin');
INSERT INTO cotacoes (`symbol`, `name`, `value`, `type`) VALUES ('CAD', 'Canadian Dollar', 3.57, 'coin');
INSERT INTO cotacoes (`symbol`, `name`, `value`, `type`) VALUES ('EUR', 'Euro', 5.20, 'coin');

INSERT INTO cotacoes (`symbol`, `name`, `value`, `type`) VALUES ('BTC-USD', 'Bitcoin', 67500.53, 'crypto');
INSERT INTO cotacoes (`symbol`, `name`, `value`, `type`) VALUES ('ETH-USD', 'Ethereum', 1020.35, 'crypto');
INSERT INTO cotacoes (`symbol`, `name`, `value`, `type`) VALUES ('SOL-USD', 'Solana', 150.36, 'crypto');
