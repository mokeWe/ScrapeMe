import re
import urllib.request
from bs4 import BeautifulSoup
import requests
import random
import os
import threading


class Cog:
    def __init__(self):
        pass

    # Ping function
    def ping(url):
        try:
            response = urllib.request.urlopen(url)
            return True
        except urllib.request.URLError as e:
            return False

    # Get HTML
    def get_html(url):
        r = requests.get(url)
        html = r.text
        html = html.encode("ascii", "ignore").decode("utf-8", "ignore")
        return html

    # Get links
    def get_links(rawText):
        soup = BeautifulSoup(rawText, "html.parser")
        return [link.get("href") for link in soup.find_all("a") if link.get("href")]

    # Get images
    def get_images(rawText):
        soup = BeautifulSoup(rawText, "html.parser")
        images = [img for img in soup.findAll("img")]
        folder = "images"
        if not os.path.exists(folder):
            os.makedirs(folder)
            for img in images:
                try:
                    image = img["src"]
                    filename = image.split("/")[-1]
                    urllib.request.urlretrieve(image, os.path.join(folder, filename))
                    print("Saved " + filename)
                except:
                    print("Failed to save " + filename)
        return images

    # Get phones
    def get_phones(rawText):
        phoneRegex = re.compile(r"""((\s|-|\.)?(\d{3})(\s|-|\.)(\d{4}))""", re.VERBOSE)
        return phoneRegex.findall(rawText)

    # Get emails
    def get_emails(rawText):
        emailRegex = re.compile(
            r"""([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+(\.[a-zA-Z]{2,4}))""", re.VERBOSE
        )
        return emailRegex.findall(rawText)

    # Write data to files.
    def write_to_file(data, file_name):
        random_name = str(random.randint(1, 100)) + "_" + file_name
        with open(random_name, "w") as text_file:
            if data != None:
                for item in data:
                    text_file.write(str(item) + "\n")
        return random_name
