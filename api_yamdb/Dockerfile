#FROM python:3.7-slim
#
#WORKDIR /app
#
#COPY requirements.txt /app
#
#RUN pip3 install -r requirements.txt --no-cache-dir
#
#COPY . /app
#
#CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000" ]

#FROM python:3.7-slim
#
#WORKDIR /app
#
#COPY . .
#
#RUN python -m pip install --upgrade pip
#RUN pip3 install -r requirements.txt --no-cache-dir
#
#CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000" ]

#FROM python:3.7-slim
#
#WORKDIR /app
#
#COPY . .
#
#RUN pip3 install -r requirements.txt --no-cache-dir
#
#CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000" ]
#
#LABEL author='mariia.bulatova@yandex.ru' version=2 broken_keyboards=100600
#
#ENV DATABASE_NAME postgres
#ENV DATABASE_PORT 5432

FROM python:3.7-slim
WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r requirements.txt --no-cache-dir
COPY ./ /app
CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000" ]
