FROM nginx:1.24

WORKDIR /usr/share/nginx/html

RUN apt-get update && \
    apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && \
    apt-get install -y nodejs

COPY ./application /var/tmp/tmp-src-app

COPY ./nginx/nginx.conf /etc/nginx/nginx.conf

RUN cd /var/tmp/tmp-src-app && npm install && npm run build

RUN cp -r /var/tmp/tmp-src-app/dist/* ./
RUN rm -rf /var/tmp/tmp-src-app

RUN chown -R nginx:nginx /usr/share/nginx/html
RUN service nginx restart

EXPOSE 3003
