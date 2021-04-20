FROM tiangolo/uwsgi-nginx:python3.7
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
# we might not need run.sh -- let's see
RUN chmod 755 start.sh 
CMD ["./start.sh"]
