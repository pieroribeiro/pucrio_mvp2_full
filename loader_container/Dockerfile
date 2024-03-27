FROM node:18

WORKDIR /usr/src/app-002

ENV APP_MODEL_HOST=model_host
ENV APP_MODEL_PORT=3001

COPY ./application .
RUN npm install

CMD ["node", "main.js"]