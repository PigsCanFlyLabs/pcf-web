FROM python:3.9-buster

# install nginx
RUN apt-get update && apt-get install nginx vim emacs -y --no-install-recommends
COPY /conf/nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

# copy source and install dependencies
RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/pip_cache
COPY main /opt/app/
COPY static /opt/app/
COPY pigscanfly /opt/app/
COPY requirements.txt /opt/apt
COPY scripts/start-server.sh /opt/app
WORKDIR /opt/app
RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir
RUN chown -R www-data:www-data /opt/app

# start server
EXPOSE 8020
STOPSIGNAL SIGTERM
CMD ["/opt/app/start-server.sh"]
