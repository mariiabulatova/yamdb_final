FROM python:3.7-slim

# RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt /app
RUN pip3 install --no-cache-dir -r requirements.txt # порядок внутри команды?

COPY ./ /app
CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000" ]

LABEL author='mariia.bulatova@yandex.ru' version=2 broken_keyboards=100600

ENV DATABASE_NAME postgres
ENV DATABASE_PORT 5432


