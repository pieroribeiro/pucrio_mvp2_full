
FROM bitnami/python:latest
WORKDIR /app
COPY ./app .
RUN pip install -r requirements.txt
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "3001", "--reload"]