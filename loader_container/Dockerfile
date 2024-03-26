FROM node:18

WORKDIR /usr/src/app-002

COPY ./application/package*.json ./

RUN npm install

COPY ./application .

ENV APP_MODEL_PORT=3001

RUN apt-get update && apt-get -y install cron

RUN echo "*/5 * * * * npm run load_coin" > /etc/cron.d/node_cron
RUN echo "*/5 * * * * npm run load_crypto" >> /etc/cron.d/node_cron
RUN echo "*/10 * * * * npm run load_news" >> /etc/cron.d/node_cron

CMD cron && tail -f /dev/null