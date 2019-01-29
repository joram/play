FROM nginx:1.15.2-alpine

RUN apk add --no-cache \
    supervisor \
    python3 \
    build-base \
    postgresql-dev \
    python3-dev \
    musl-dev && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH="${PYTHONPATH}:/app" \
    DJANGO_SETTINGS_MODULE="settings.base"

WORKDIR /app

ADD requirements.dev.txt /app/requirements.dev.txt
ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.dev.txt

COPY ./play \
    ./entrypoint.sh \
    /app/

EXPOSE 8000

CMD [ "/app/entrypoint.sh" ]
