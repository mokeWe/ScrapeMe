import re
import urllib.request
from bs4 import BeautifulSoup
import requests
import random

# Ping function
def ping(url):
    try:
        response = urllib.request.urlopen(url)
        return True
    except urllib.request.URLError as e:
        return False


# Get HTML
def get_html(url):
    try:
        r = requests.get(url)
        html = r.text
        html = html.encode("ascii", "ignore").decode("utf-8", "ignore")
        return html
    except requests.exceptions.ConnectionError:
        return False


# Get links
def get_links(rawText):
    soup = BeautifulSoup(rawText, "html.parser")
    return [
        link.get("href") for link in soup.find_all("a") if link.get("href") is not None
    ]


# Get images
def get_images(rawText):
    soup = BeautifulSoup(rawText, "html.parser")
    return [
        link.get("src") for link in soup.find_all("img") if link.get("src") is not None
    ]


# Get phones
def get_phones(rawText):
    phoneRegex = re.compile(
        r"""(
        (\s|-|\.)?                      # separator
        (\d{3})                         # first 3 digits
        (\s|-|\.)                       # separator
        (\d{4})                         # last 4 digits
        )""",
        re.VERBOSE,
    )
    return phoneRegex.findall(rawText)


# Get emails
def get_emails(rawText):
    emailRegex = re.compile(
        r"""(
        [a-zA-Z0-9._%+-]+      # username
        @                      # @ symbol
        [a-zA-Z0-9.-]+         # domain name
        (\.[a-zA-Z]{2,4})      # dot-something
        )""",
        re.VERBOSE,
    )
    return emailRegex.findall(rawText)


# Write data to files.
def write_to_file(data, file_name):
    random_name = str(random.randint(1, 100)) + "_" + file_name
    with open(random_name, "w") as text_file:
        if data != None:
            for item in data:
                text_file.write(item + "\n")
    return random_name
