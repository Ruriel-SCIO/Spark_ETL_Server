from .metadataLoader import _MetadataLoader
from .sparkSessionLoader import _SparkSessionLoader
from ioOperations import compression, jsonFileFormatter
from os.path import basename
from os import makedirs
from uuid import uuid4
from tempfile import gettempdir as getTempDir
from shutil import copyfile
from pyspark.sql.types import StringType, FloatType, LongType
from pyspark.sql.functions import col, unix_timestamp as unixTimestamp

_TYPE_SWITCHER = {
    'float': FloatType(),
    'long': LongType(),
    'text': StringType()
}


class ETL:

    def __init__(self):
        self.metadata = _MetadataLoader().getMetadata()
        self.spark = _SparkSessionLoader().getSparkSession()
        self.tempFolder = '{}/{}/{}'.format(getTempDir(),'spark_etl_server', uuid4())
    # Reads the file to be processed. If it's compressed, uncompress in the temp folder and return it's location.
    # Otherwise, simply copies it to the temp folder.

    def preProcessing(self, fileLocation):
        metadata = self.metadata
        outputFilename = basename(fileLocation)
        makedirs(self.tempFolder, exist_ok=True)
        if 'compression' in metadata:
            length = len(outputFilename)
            outputFileLocation = '{}/{}'.format(self.tempFolder,outputFilename[:length-3])
            compression.decompress(fileLocation, outputFileLocation)
        else:
            outputFileLocation = '{}/{}'.format(self.tempFolder, outputFilename)
            copyfile(fileLocation, outputFileLocation)
        return outputFileLocation

    #Loads the file into a dataframe.
    def loadData(self, fileLocation):
        self._dataframe = self.spark.read.options(
            inferSchema=True).json(fileLocation, multiLine=True)

    #Drops all the columns from the dataframe not present in the metadata file.
    def cleanDataframe(self):
        valid_columns = [dimension['name'] for dimension in self.metadata['fact']['dimensions']]
        drop_columns = [column_name for column_name in self._dataframe.columns if not column_name in valid_columns]
        self._dataframe = self._dataframe.drop(*drop_columns)

    #Converts each column in the dataframe into a type specified in the metadata.
    def convertDataframe(self):
        for dimension in self.metadata['fact']['dimensions']:
            dimension_type = dimension['type'] if 'type' in dimension else 'text'
            if type(dimension_type) is str:
                type_cast = _TYPE_SWITCHER.get(dimension_type, StringType())
                column = col(dimension['value']).cast(type_cast)
            elif dimension_type['source'] == 'duration':
                if dimension_type['destination'] == 'long':
                    column = unixTimestamp(dimension['value'], dimension_type['format'])
                else:
                    column = col(dimension['value']).cast(StringType())
            self._dataframe = self._dataframe.withColumn(dimension['name'], column)
        self.cleanDataframe()
    
    def writeDataframeJson(self):
        convertedDataframeFolder = '{}/{}'.format(self.tempFolder, 'convertedDataframe')
        outputJSONFileName = '{}/{}'.format(self.tempFolder, 'convertedDataframe.json')
        compressedJSONFileName = '{}.{}'.format(outputJSONFileName, 'gz')
        self._dataframe.write.mode("overwrite").format('json').save(convertedDataframeFolder)
        jsonFileFormatter.formatFile(convertedDataframeFolder, outputJSONFileName)
        compression.compress(outputJSONFileName, compressedJSONFileName)
        return compressedJSONFileName