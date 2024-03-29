FROM node:18

WORKDIR /usr/src/app-002

ENV APP_MODEL_HOST=model_host
ENV APP_MODEL_PORT=3001
ENV TIME_TO_EXEC_COIN="*/1 * * * *"
ENV TIME_TO_EXEC_CRYPTO="*/1 * * * *"
ENV TIME_TO_EXEC_NEWS="*/1 * * * *"

COPY ./application .
RUN npm install

CMD ["node", "main.js"]