FROM python:3.8.5
WORKDIR /code
RUN pip install --upgrade pip
COPY . .
RUN pip install wheel
RUN pip install -r requirements.txt
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000