FROM python:3.8-alpine

WORKDIR /usr/src/app
COPY . /usr/src/app

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install -r requirements.txt

EXPOSE 5005

CMD ["python", "manage.py"]
