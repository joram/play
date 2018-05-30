FROM alpine:3.7

RUN apk add --no-cache python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache


RUN mkdir /battlesnakeio_play
RUN cd /battlesnakeio_play
ENV PYTHONPATH="${PYTHONPATH}:/battlesnakeio_play"
ENV DJANGO_SETTINGS_MODULE="settings.settings"
WORKDIR /battlesnakeio_play

ADD requirements.txt /battlesnakeio_play/requirements.txt
RUN pip install -r /battlesnakeio_play/requirements.txt

COPY ./play /battlesnakeio_play/

RUN ls -r /battlesnakeio_play

EXPOSE 8000
CMD ["gunicorn", "wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
