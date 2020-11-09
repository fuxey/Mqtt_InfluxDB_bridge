FROM python:alpine3.8

WORKDIR /app

COPY ./app/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY app/ /app
RUN ls -la /app/*

EXPOSE 8000
CMD ["python", "run.py"]
