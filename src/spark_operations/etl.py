from .metadata_loader import _MetadataLoader
from .spark_session_loader import _SparkSessionLoader
from io_operations import compression
from os.path import basename
from os import makedirs
from uuid import uuid4
from tempfile import gettempdir
from shutil import copyfile
from pyspark.sql.types import StringType, FloatType, LongType
from pyspark.sql.functions import col, unix_timestamp

_TYPE_SWITCHER = {
    'float': FloatType(),
    'long': LongType(),
    'text': StringType()
}


class ETL:

    def __init__(self):
        self.metadata = _MetadataLoader().get_metadata()
        self.spark = _SparkSessionLoader().get_spark_session()

    # Reads the file to be processed. If it's compressed, uncompress in the temp folder and return it's location.
    # Otherwise, simply copies it to the temp folder.

    def pre_processing(self, fileLocation):
        metadata = self.metadata
        outputFolder = '{}/{}/{}'.format(gettempdir(),'spark_etl_server', uuid4())
        outputFilename = basename(fileLocation)
        makedirs(outputFolder, exist_ok=True)
        if 'compression' in metadata:
            length = len(outputFilename)
            outputFileLocation = '{}/{}'.format(outputFolder,outputFilename[:length-3])
            compression.decompress(fileLocation, outputFileLocation)
        else:
            outputFileLocation = '{}/{}'.format(outputFolder, outputFilename)
            copyfile(fileLocation, outputFileLocation)
        return outputFileLocation

    #Loads the file into a dataframe.
    def load_data(self, fileLocation):
        self._dataframe = self.spark.read.options(
            inferSchema=True).json(fileLocation, multiLine=True)

    #Drops all the columns from the dataframe not present in the metadata file.
    def clean_dataframe(self):
        valid_columns = [dimension['name'] for dimension in self.metadata['fact']['dimensions']]
        drop_columns = [column_name for column_name in self._dataframe.columns if not column_name in valid_columns]
        self._dataframe = self._dataframe.drop(*drop_columns)

    #Converts each column in the dataframe into a type specified in the metadata.
    def convert_dataframe(self):
        for dimension in self.metadata['fact']['dimensions']:
            dimension_type = dimension['type'] if 'type' in dimension else 'text'
            if type(dimension_type) is str:
                type_cast = _TYPE_SWITCHER.get(dimension_type, StringType())
                column = col(dimension['value']).cast(type_cast)
            elif dimension_type['source'] == 'duration':
                if dimension_type['destination'] == 'long':
                    column = unix_timestamp(dimension['value'], dimension_type['format'])
                else:
                    column = col(dimension['value']).cast(StringType())
            self._dataframe = self._dataframe.withColumn(dimension['name'], column)
        self.clean_dataframe()