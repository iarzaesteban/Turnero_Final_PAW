FROM python:3.12.1-alpine3.18

RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-dev \
    python3-dev \
    libffi-dev \
    chromium \
    graphviz \
    graphviz-dev

WORKDIR /code/

RUN pip install --upgrade pip \
    && pip install gunicorn

COPY deploy/requirements/requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt

COPY ./ /code/

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.wsgi:application"]
