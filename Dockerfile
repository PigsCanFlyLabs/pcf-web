FROM python:3.9-buster

# install nginx
RUN apt-get update && apt-get install nginx vim emacs libmariadbclient-dev default-libmysqlclient-dev libssl-dev -y
COPY /conf/nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

# copy source and install dependencies
RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/pip_cache
COPY main /opt/app/main
COPY static /opt/app/static
COPY pigscanfly /opt/app/pigscanfly
COPY requirements.txt /opt/app/
COPY scripts/start-server.sh /opt/app/
COPY *.py /opt/app/
WORKDIR /opt/app/
RUN pip install --upgrade pip && pip install -r /opt/app/requirements.txt
RUN chown -R www-data:www-data /opt/app

# start server
EXPOSE 80
STOPSIGNAL SIGTERM
CMD ["/opt/app/start-server.sh"]
