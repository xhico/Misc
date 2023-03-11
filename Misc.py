# -*- coding: utf-8 -*-
# !/usr/bin/python3

import base64
import json


def get911(key):
    """
    Given a key, reads a file located at /home/pi/.911 that contains encoded JSON data.
    Decodes the data and returns the value of the given key.

    Parameters:
    -----------
    key : str
        A string representing the key to be looked up in the decoded JSON data.

    Returns:
    --------
    str or dict or list or int or float or bool or None
        The value of the given key in the decoded JSON data.

    Raises:
    -------
    FileNotFoundError
        If the file at /home/pi/.911 does not exist or cannot be opened.
    KeyError
        If the given key is not found in the decoded JSON data.
    JSONDecodeError
        If the decoded data is not valid JSON.
    """
    # Open the file at /home/pi/.911 in read mode and decode its contents
    with open("/home/pi/.911") as inFile:
        # Read the contents of the file and decode from base64 encoding
        # Decode the resulting bytes using utf-8 encoding and load the JSON data
        data = json.loads(base64.b64decode(inFile.read().encode("utf-8")).decode("utf-8"))

    # Look up the given key in the decoded JSON data and return its value
    return data[key]
