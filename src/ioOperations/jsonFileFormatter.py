from os import listdir
from shutil import rmtree

def _decodeLine(line):
    line = line.replace("\"[", "[")
    line = line.replace("]\"", "]")
    line = line.encode('latin1', 'backslashreplace').decode('unicode-escape')
    line = line.replace("\"{", "{")
    line = line.replace("}\"", "}")
    return line


def formatFile(tempFolder, outputLocation):
    tmpFileList = listdir(tempFolder)
    if '_SUCCESS' in tmpFileList:
        with open(outputLocation, 'w') as output:
            isFirstLine = True
            output.write('[')
            for tmpFileName in tmpFileList:
                if tmpFileName.endswith(".json"):
                    tmpFileLocation = tempFolder+'/'+tmpFileName
                    with open(tmpFileLocation) as tmpFile:
                        for line in tmpFile:
                            line = line.strip()
                            if len(line) > 0:
                                if isFirstLine:
                                    isFirstLine = False
                                else:
                                    output.write(',')
                                output.write(_decodeLine(line))
            output.write(']')
        rmtree(tempFolder)
        return True
    else:
        return False