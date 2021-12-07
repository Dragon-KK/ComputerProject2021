import sys
from pathlib import Path
import json

PARENT_PATH = Path(__file__).parent.parent.parent.joinpath('data')

def getRawText(filename,*options,**kwargs):
    return PARENT_PATH.joinpath(filename).read_text(*options,**kwargs)

def getRawBytes(filename,*options,**kwargs):
    return PARENT_PATH.joinpath(filename).read_bytes(*options,**kwargs)

def getJson(filename):
    return json.loads(PARENT_PATH.joinpath(filename).read_text())

def saveJson(filename, obj):
    PARENT_PATH.joinpath(filename).write_text(json.dumps(obj))

def saveText(filename, data):
    PARENT_PATH.joinpath(filename).write_text(data)

def saveBytes(filename, data):
    PARENT_PATH.joinpath(filename).write_bytes(data)