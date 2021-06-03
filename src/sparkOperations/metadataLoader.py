from json import load as jsonLoad
from os import getenv

class _MetadataLoader:
    def __init__(self):
        metadataFile = open(getenv('METADATA_FILE'))
        self._metadata = jsonLoad(metadataFile)
        metadataFile.close()

    def getMetadata(self):
        return self._metadata
