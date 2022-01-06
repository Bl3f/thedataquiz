FROM python:3.10

WORKDIR /code

# install django
COPY requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt

# copy application code
COPY . /code/

EXPOSE 8000
CMD ./manage.py runserver 0.0.0.0:80
