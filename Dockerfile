FROM python:3.9.5 AS build
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.9.5-slim
ENV PROJECT_FOLDER /app
WORKDIR ${PROJECT_FOLDER}

COPY --from=build /root/.local /root/.local
COPY src/ ${PROJECT_FOLDER}/src/
ENV PATH=/root/.local:$PATH
ENTRYPOINT [ "python3", "src/main.py" ]
