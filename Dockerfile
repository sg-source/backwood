FROM python:3.9-slim

COPY . /backwood
WORKDIR /backwood

RUN  chmod +x ./entrypoint.sh && python -m pip install --upgrade pip &&  \
     pip install -r requirements.txt

ENTRYPOINT ["./entrypoint.sh"]

CMD ["python", "./src/manage.py", "runserver",  "0.0.0.0:8080"]