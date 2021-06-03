FROM python:3.9.5

ENV PYTHONPATH /usr/local/project
ENV DATALAKE ${PYTHONPATH}/datalake
ENV JSON_FILE ${DATALAKE}/generated.json.gz
ENV CONFIG ${PYTHONPATH}/config
ENV METADATA_FILE ${CONFIG}/metadata.json
ENV DRUID_SERVER http://localhost:8888/druid/indexer/v1/task

WORKDIR ${PYTHONPATH}
COPY requirements.txt ${PYTHONPATH}/
RUN pip install -r requirements.txt

COPY src/ ${PYTHONPATH}/src/
COPY datalake/ ${DATALAKE}/
COPY config/ ${CONFIG}/

RUN python3 ${PYTHONPATH}/src/main.py

