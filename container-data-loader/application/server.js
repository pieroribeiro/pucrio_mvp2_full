const app = require('./app')

app.listen(process.env.APP_PORT, () => {
  console.log(`API service is running on port "${process.env.APP_PORT}"!`);
})