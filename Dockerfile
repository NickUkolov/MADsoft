FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements_api.txt /tmp/requirements_api.txt

RUN pip install --upgrade pip && pip3 --no-cache-dir install --prefer-binary -r /tmp/requirements_api.txt && rm /tmp/requirements_api.txt

RUN addgroup --gid 1000 notroot && \
    useradd -u 1000 -g notroot notroot -m

RUN mkdir /opt/api

COPY --chown=notroot:notroot ./api /opt/api

USER notroot
WORKDIR /opt/api
RUN chmod +x /opt/api/entrypoint_api.sh

EXPOSE $API_PORT

CMD ["./entrypoint_api.sh"]
