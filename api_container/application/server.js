const app = require('./app')

app.listen(process.env.APP_PORT || 8080, () => {
  console.log(`API service is running on port "${process.env.APP_PORT}"!`);
})