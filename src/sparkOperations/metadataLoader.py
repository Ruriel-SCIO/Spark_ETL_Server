from dotenv import load_dotenv as loadDotEnv
from json import load as jsonLoad
from os import getenv


class _MetadataLoader:
    def __init__(self):
        loadDotEnv()
        metadataFile = open(getenv('metadataFile'))
        self._metadata = jsonLoad(metadataFile)
        metadataFile.close()

    def getMetadata(self):
        return self._metadata
