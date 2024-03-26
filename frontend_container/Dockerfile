FROM nginx:1.24

COPY ./application /usr/share/nginx/html
COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
RUN chown -R nginx:nginx /usr/share/nginx/html
RUN service nginx restart

EXPOSE 3003

ENV APP_PORT=3003
