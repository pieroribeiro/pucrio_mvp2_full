FROM node:18

WORKDIR /usr/src/app-001

COPY ./application .

RUN npm install

CMD ["npm", "run", "start"]

EXPOSE 3002

ENV APP_PORT=3002