FROM python:3.9-alpine

WORKDIR /app/

COPY requirements.txt /app/

RUN apk update && \
    pip install -r requirements.txt

COPY . /app/

CMD ["python","main.py"]
