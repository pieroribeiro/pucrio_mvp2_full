FROM node:18

WORKDIR /usr/src/app-001

COPY ./application .

ENV APP_INTERCEPTOR_HOST=interceptor_host
ENV APP_INTERCEPTOR_PORT=3001
ENV APP_PORT=3002

RUN npm install

CMD ["npm", "run", "start"]

EXPOSE 3002
