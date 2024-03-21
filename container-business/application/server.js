const express = require('express');
const app = express();

app.get('/', (req, res) => {
  res.send('Olá, mundo!');
});

app.listen(process.env.APP_PORT, () => {
  console.log(`Servidor rodando na porta ${process.env.APP_PORT}`);
});