from sparkOperations.etl import ETL
from dotenv import load_dotenv as loadDotEnv
from rest.api import sendToDruid
if __name__ == "__main__":
    loadDotEnv()
    print("Starting ETL module...")
    etl = ETL()
    print("Pre-processing file...")
    fileLocation = etl.preProcessing('./datalake/generated.json.gz')
    print("Loading file into dataframe...")
    etl.loadData(fileLocation)
    print("Initializing dataframe convertion...")
    etl.convertDataframe()
    print("Saving dataframe to JSON file...")
    convertedJSONFile = etl.writeDataframeJson()
    print("Sending file to Druid...")
    response = sendToDruid(etl.metadata, convertedJSONFile)
    print("Done.")