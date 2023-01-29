FROM python:3.7-slim
LABEL author='Denis Murashov' project_name='urls_shortner' version='1.0'

WORKDIR /app

COPY ../ /app

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir
RUN python manage.py makemigrations

CMD ["gunicorn", "link_shorter.wsgi:application", "--bind", "0:8000"]