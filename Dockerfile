FROM datamechanics/spark:3.1.1-latest AS build
COPY requirements.txt .
RUN pip install --user -r requirements.txt

ENV PROJECT_FOLDER /app
WORKDIR ${PROJECT_FOLDER}

COPY src/ ${PROJECT_FOLDER}/src/
CMD [ "python", "src/main.py" ]
