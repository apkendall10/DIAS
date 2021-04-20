FROM tiangolo/uwsgi-nginx:python3.7
WORKDIR /app
COPY . /app
RUN pip install -r /app/requirements.txt
COPY nginx.conf /etc/nginx
# we might not need run.sh -- let's see
RUN chmod 755 /app/start.sh
CMD ["/app/start.sh"]
