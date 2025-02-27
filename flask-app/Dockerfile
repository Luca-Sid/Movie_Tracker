FROM python:3.12-bookworm

WORKDIR /movie_tracker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV DB_NAME='movie_tracker'
ENV DB_PORT=3306

CMD ["gunicorn", "-b 0.0.0.0:80", "app:app"]
# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]