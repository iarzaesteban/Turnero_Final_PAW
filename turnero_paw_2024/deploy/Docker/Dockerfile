FROM python:3.12.1-alpine3.18

WORKDIR /code/

RUN apk update \ 
    && apk add --no-cache gcc musl-dev postgresql-dev python3-dev libffi-dev \
    && pip install --upgrade pip

COPY deploy/requirements/requirements.txt /code/requirements.txt

RUN pip install -r requirements.txt

COPY ./ ./

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]