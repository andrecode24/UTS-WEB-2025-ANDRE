ARG PYTHON_VERSION=3.13-slim

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code

WORKDIR /code

COPY requirements.txt /tmp/requirements.txt
RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/
COPY . /code

ENV SECRET_KEY "laYy9iYUxvUy0V6KnBuzrElwWkCK1LnrUU7dG40fwPOJ9HOHkb"
RUN python manage.py migrate --noinput
RUN python manage.py seed_data

EXPOSE 8000

CMD ["gunicorn","--bind",":8000","--workers","2","coop_prasetiya_mulya.wsgi"]
