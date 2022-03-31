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
CMD ["python", "manage.py", "makemigrations"]
CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]