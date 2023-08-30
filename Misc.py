# -*- coding: utf-8 -*-
# !/usr/bin/python3

import base64
import json
import socket

import yagmail


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


def sendErrorEmail(script, msg):
    """
    Sends an error email notification using Yagmail.

    This function sends an email to the designated receiver to notify about an error
    that occurred during script execution. The email subject includes the hostname,
    the word "Error," and the name of the script that encountered the error.

    Args:
        script (str): The name or identifier of the script where the error occurred.
        msg (str): The error message or details to be included in the email body.

    Returns:
        None

    Raises:
        None

    Note:
        - This function requires Yagmail to be properly configured with the sender's
          email credentials and the appropriate permissions.
        - The email configuration is retrieved using the 'get911' function, which
          should be defined elsewhere in the code.
    """
    # Get the uppercase hostname of the current machine
    hostname = str(socket.gethostname()).upper()

    # Retrieve necessary email configuration using 'get911'
    EMAIL_USER = get911('EMAIL_USER')
    EMAIL_APPPW = get911('EMAIL_APPPW')
    EMAIL_RECEIVER = get911('EMAIL_RECEIVER')

    # Initialize a Yagmail SMTP instance
    YAGMAIL = yagmail.SMTP(EMAIL_USER, EMAIL_APPPW)

    # Send the error email
    YAGMAIL.send(EMAIL_RECEIVER, f"{hostname} - Error - {script}", msg)
