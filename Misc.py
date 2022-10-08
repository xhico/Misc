# -*- coding: utf-8 -*-
# !/usr/bin/python3
import base64
import json


def get911(key):
    with open("/home/pi/.911") as inFile:
        data = json.loads(base64.b64decode(inFile.read().encode('ascii')).decode('ascii'))
    return data[key]
