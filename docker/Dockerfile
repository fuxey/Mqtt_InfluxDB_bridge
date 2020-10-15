FROM python:alpine3.8

WORKDIR /app
COPY . /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["python", "run.py"]
