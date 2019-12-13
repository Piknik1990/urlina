FROM python:3

WORKDIR /usr/src/app

RUN pip install --no-cache-dir PyYAML requests

COPY urlina3.py /usr/src/app

ENTRYPOINT [ "./urlina3.py" ]

