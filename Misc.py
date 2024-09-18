# -*- coding: utf-8 -*-
# !/usr/bin/python3

import base64
import json
import os
import socket
import subprocess

import requests
import yagmail


def detectInternetInterface():
    """
    Detects the internet interface by executing the 'nmcli c' command and parsing the output.

    The function uses subprocess to run the 'nmcli c' command, extracts the second line of the output,
    and retrieves the second-to-last field, which is assumed to contain the internet interface type.

    Returns:
    str: The internet interface type.

    Note:
    Ensure that 'nmcli' is available on the system, and the command provides the expected output format.
    """
    return subprocess.getoutput("nmcli c | awk 'NR==2 {print $(NF-1)}'")


def get911(key):
    """
    Given a key, reads a file located at /home/$USER/.911 that contains encoded JSON data.
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
        If the file at /home/$USER/.911 does not exist or cannot be opened.
    KeyError
        If the given key is not found in the decoded JSON data.
    JSONDecodeError
        If the decoded data is not valid JSON.
    """

    # Get the current user's home directory
    user_home = os.path.expanduser("~")

    # Open the file at /home/$USER/.911 in read mode and decode its contents
    file_path = os.path.join(user_home, ".911")
    with open(file_path) as inFile:
        # Read the contents of the file and decode from base64 encoding
        # Decode the resulting bytes using utf-8 encoding and load the JSON data
        data = json.loads(base64.b64decode(inFile.read().encode("utf-8")).decode("utf-8"))

    # Look up the given key in the decoded JSON data and return its value
    return data[key]


def sendEmail(subject, body, attachments=None):
    """
    Sends an email notification using Yagmail.

    This function sends an email to the designated receiver.

    Args:
        subject (str): subject of email
        body (str): body of email
        attachments (str): attachments of email (optional)

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

    # Retrieve the necessary email configuration using 'get911'
    EMAIL_USER = get911("EMAIL_USER")
    EMAIL_APPPW = get911("EMAIL_APPPW")
    EMAIL_RECEIVER = get911("EMAIL_RECEIVER")

    # Initialize a Yagmail SMTP instance
    YAGMAIL = yagmail.SMTP(EMAIL_USER, EMAIL_APPPW)

    # Send the error email
    YAGMAIL.send(EMAIL_RECEIVER, f"{hostname} - {subject}", body, attachments)


def sendNotification(subject, body, attachments=None):
    """
    Sends a notification with a subject, body, and optional attachments to a specified notification service.

    Parameters:
    subject (str): The subject of the notification.
    body (str): The body of the notification.
    attachments (str, optional): The path to a file to be attached to the notification. Defaults to None.

    Returns:
    None
    """

    # Get the uppercase hostname of the current machine
    hostname = str(socket.gethostname()).upper()

    # Retrieve the necessary NTFY configuration using 'get911'
    NTFY_URL = get911("NTFY_URL")
    NTFY_TOKEN = get911("NTFY_TOKEN")

    # Prepare headers for the request, including authorization and the title with hostname and subject
    headers = {"Authorization": f"Bearer {NTFY_TOKEN}", "Title": f"{hostname} - {subject}"}

    # Prepare the data for the request; if there are attachments, read the file in binary mode
    data = f"{body}" if not attachments else open(attachments, "rb")

    # Send the notification via a POST request to the specified NTFY_URL
    requests.post(NTFY_URL, data=data, headers=headers)
