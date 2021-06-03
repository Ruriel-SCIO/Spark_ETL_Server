import gzip
import shutil

def compress(inputLocation, outputLocation):
    with open(inputLocation, 'rb') as input:
        with gzip.open(outputLocation, 'wb') as output:
            shutil.copyfileobj(input, output)

def decompress(inputLocation, outputLocation):
    with gzip.open(inputLocation, 'rb') as compressedFile:
        with open(outputLocation, 'wb') as output:
            shutil.copyfileobj(compressedFile, output)