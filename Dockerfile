
FROM python:3.10.0

MAINTAINER Sergio Bruni "sergio.bruni@ingv.it"

ENV PYTHONUNBUFFERED 1
WORKDIR /opt
RUN mkdir -p log
RUN chmod -R 777 /opt/log
COPY . .

# Install the Python libraries
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# COPY uswgi.ini
COPY ./uwsgi.ini /etc/uwsgi.ini

EXPOSE 5000

# run server
CMD ["./entrypoint.sh"]
