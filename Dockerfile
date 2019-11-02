FROM python:latest

RUN pip install --upgrade pip

RUN adduser --disabled-password --gecos '' python

LABEL owner = jgoralcz
LABEL serviceVersion = 0.1.0
LABEL description = "Parsing JSON and Storing SQLite"

COPY --chown=python:python config.json /usr/src/python/
COPY --chown=python:python requirements.txt /usr/src/python/
COPY --chown=python:python src/ /usr/src/python/src/

ENV PATH="/home/python/.local/bin:${PATH}"

WORKDIR /usr/src/python

USER python

RUN pip install --user -r requirements.txt

CMD ["python", "src/read_data.py"]