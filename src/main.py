from spark_operations.etl import ETL
if __name__ == "__main__":
    etl = ETL()
    fileLocation = etl.pre_processing('./datalake/generated.json.gz')
    etl.load_data(fileLocation)
    etl.convert_dataframe()