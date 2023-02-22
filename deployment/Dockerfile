FROM python:3.9-slim

COPY ./ /backwood
WORKDIR /backwood

RUN mkdir -p /var/log/gunicorn
RUN pip install -r requirements.txt && python ./src/manage.py makemigrations && python ./src/manage.py migrate && python ./src/manage.py loaddata ./src/utils/db.json

ENTRYPOINT ["gunicorn"]

CMD ["-c", "deployment/gunicorn/dev.py"]