from spark_operations.etl import ETL
if __name__ == "__main__":
    etl = ETL()
    fileLocation = etl.pre_processing('./datalake/generated.json.gz')
    print(fileLocation)