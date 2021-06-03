import requests
from os.path import dirname, basename
from os import getenv


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
                    "dimensionExclusions" : [timestampColumn["column"]]
                },
                "granularitySpec": {
                    "segmentGranularity": "day",
                    "queryGranularity": "none",
                    "rollup": True
                },
                "metricsSpec":[
                    { "type": "count", "name": "count"}
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


def sendToDruid(metadata, jsonFolder):
    body = _prepareRequest(metadata, jsonFolder)
    druidServer = getenv("DRUID_SERVER")
    response = requests.post(druidServer, json=body)
    print('Response: {}'.format(response.text))
    return response
