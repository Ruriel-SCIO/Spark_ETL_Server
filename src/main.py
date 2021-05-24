from sparkOperations.etl import ETL
if __name__ == "__main__":
    etl = ETL()
    fileLocation = etl.preProcessing('./datalake/generated.json.gz')
    etl.loadData(fileLocation)
    etl.convertDataframe()
    convertedJSON = etl.writeDataframeJson()