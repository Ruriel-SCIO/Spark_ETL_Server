import requests
from os.path import dirname, basename
from os import getenv
from time import sleep
def _prepareRequest(metadata, jsonFolder):
    dimensions = []
    timestampColumn = None

    for column in metadata['fact']['dimensions']:
        if "isTimeDimension" in column and column['isTimeDimension']:
            timestampColumn = {
                "column": column["name"],
                "format": column["format"]
            }
        else:
            if("type" not in column or type(column["type"]) is str):
                fieldType = "string" if "type" not in column else column["type"]
            else:
                fieldType = column["type"]["destination"]
            dimensions.append({
                "type": fieldType,
                "name": column["name"]
            })

    requestBody = {
        "type": "index_parallel",
        "spec": {
            "dataSchema": {
                "dataSource": metadata['fact']['name'],
                "timestampSpec": timestampColumn,
                "dimensionsSpec": {
                    "dimensions": dimensions,
                    "dimensionExclusions": [timestampColumn["column"]]
                },
                "granularitySpec": {
                    "segmentGranularity": "day",
                    "queryGranularity": "day",
                    "rollup": True
                },
                "metricsSpec": [
                    {"type": "count", "name": "count"}
                ]
            },
            "ioConfig": {
                "type": "index_parallel",
                "inputSource": {
                    "type": "local",
                    "baseDir": dirname(jsonFolder),
                    "filter": basename(jsonFolder)
                },
                "inputFormat": {
                    "type": "json"
                }
            },
            "tuningConfig": {
                "type": "index_parallel"
            }
        }
    }
    return requestBody

def waitForStatus():
    sleepTime=0.5
    retries=10
    success=False
    while success == False and retries > 0:
        try:
            response = requests.get("http://localhost:8888/status")
            if response.status_code == 200 and "error" not in response:
                success = True
        except requests.exceptions.ConnectionError:
            print('Druid is not available. Waiting {} seconds and trying again.'.format(sleepTime))
            sleep(0.5)
            sleepTime*=2
            retries-=1
    return success

def sendToDruid(metadata, jsonFolder):
    body = _prepareRequest(metadata, jsonFolder)
    druidServer = getenv("DRUID_SERVER")
    print('Testing if Druid is available.')
    if waitForStatus():
        print("Sending file to Druid...")
        response = requests.post(druidServer, json=body)
        print('Response: {}'.format(response.text))
        return response
    else:
        return 'Druid wasn\'t available in time'