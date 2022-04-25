FROM python:3.9-alpine

COPY requirements.txt .
RUN python3 -m pip install -r \
    requirements.txt --quiet --no-cache-dir \
    && rm -f requirements.txt

ADD . /workspace
WORKDIR /workspace

ENTRYPOINT [ "python" ]
CMD [ "main.py" ]

