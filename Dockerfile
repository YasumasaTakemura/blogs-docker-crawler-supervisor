FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean && \
    ln -sf /usr/bin/python3 /usr/bin/python && \
    ln -sf /usr/bin/pip3 /usr/bin/pip

# crawler application
COPY ./ /src

# python
RUN pip install --upgrade pip
RUN pip install -r /src/requirements.txt

# uwsgi
RUN touch /src/reload.trigger && \
    if [ ! -d "/var/log/uwsgi" ] ; then mkdir /var/log/uwsgi ; fi

WORKDIR /src

CMD ["uwsgi","--ini","uwsgi.ini"]