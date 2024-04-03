FROM python:3.8
WORKDIR /app
COPY ./app .
RUN pip install -r requirements.txt
CMD ["flask", "--app", "__init__.py", "run", "--host", "0.0.0.0", "--port", "3001", "--reload"]
EXPOSE 3001
ENV APP_PORT=3001
ENV DB_HOST=database_host
ENV DB_DATABASE=mvp2
ENV DB_USER=app
ENV DB_PASSWORD=app142536