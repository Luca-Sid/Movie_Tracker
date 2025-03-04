FROM python:3.12-bookworm

WORKDIR /recommendation-service

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["gunicorn", "-b 0.0.0.0:80", "app:app"]
