
FROM python:3.8

WORKDIR /var/lib/python/

# install FreeTDS and dependencies
RUN apt-get update \
  && apt-get install unixodbc -y \
  && apt-get install unixodbc-dev -y \
  && apt-get install freetds-dev -y \
  && apt-get install freetds-bin -y \
  && apt-get install tdsodbc -y \
  && apt-get install --reinstall build-essential -y\
  && apt-get install odbc-postgresql

# populate "ocbcinst.ini"
RUN echo "[FreeTDS]\n\
  Description = FreeTDS unixODBC Driver\n\
  Driver = /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so\n\
  Setup = /usr/lib/x86_64-linux-gnu/odbc/libtdsS.so" >> /etc/odbcinst.ini

COPY . /var/lib/python

RUN pip install -r ./requirements.txt

EXPOSE 6003

CMD ["python", "-u", "./app.py"]
