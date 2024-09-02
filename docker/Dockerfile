FROM python:3.10-bullseye

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN apt-get update && apt-get install -y netcat

COPY ./requirements.txt /requirements.txt
RUN pip install -U pip pip-tools && pip install --no-cache-dir -r /requirements.txt && rm -rf /requirements.txt

COPY ./docker/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY . /app
WORKDIR /app

RUN useradd -m -s /bin/bash usr && chown -R usr:usr /app
USER usr

ENTRYPOINT ["/entrypoint"]