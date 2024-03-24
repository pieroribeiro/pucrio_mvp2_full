FROM node:18

WORKDIR /usr/src/app

COPY ./application/package*.json ./

RUN npm install

COPY ./application .

EXPOSE 3003

CMD ["npm", "start"]
