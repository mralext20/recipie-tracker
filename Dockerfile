FROM python:3.6

RUN adduser --disabled-password --gecos "" app

WORKDIR /home/app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY app app

COPY app.py config.py boot.sh setup.py ./
RUN chmod +x boot.sh

ENV FLASK_APP app.py

RUN chown -R app:app ./
USER app

EXPOSE 5000
ENTRYPOINT ./boot.sh