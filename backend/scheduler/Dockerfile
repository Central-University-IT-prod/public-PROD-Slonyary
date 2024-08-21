FROM python:3.11.5-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY ./scheduler ./scheduler
COPY ./shared ./shared

CMD ["python", "-m", "scheduler"]
