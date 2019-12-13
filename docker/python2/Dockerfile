FROM python:2

WORKDIR /usr/src/app

RUN pip install --no-cache-dir PyYAML requests

COPY urlina.py /usr/src/app

ENTRYPOINT [ "./urlina.py" ]

