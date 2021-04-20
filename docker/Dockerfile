FROM tiangolo/uwsgi-nginx:python3.7
ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/static
COPY ./requirements.txt /var/www/requirements.txt
RUN pip install -r /var/www/requirements.txt
COPY worker.py /var/www/app/worker.py
COPY config.py /var/www/app/config.py
COPY uwsgi.ini /var/www/app/wsgi.ini
