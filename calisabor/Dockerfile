# Author Luis Angel Vargas Mosquera
FROM python:3.8
WORKDIR /calisabor
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

RUN pip install --upgrade pip wheel

RUN pip install backports.zoneinfo

COPY requirements.txt ./

RUN pip install -r requirements.txt
COPY . .

EXPOSE 8000
RUN ["python", "manage.py", "makemigrations"]
RUN ["python", "manage.py", "migrate"]
RUN echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('cs_admin', 'admin@myproject.co', 'p445w0rd')" | python manage.py shell
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]