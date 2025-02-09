FROM python:3.12-bookworm

WORKDIR /movie_tracker

COPY app/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY app/ .

CMD ["python3", "app.py"]