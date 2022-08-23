import re
import urllib.request
import os
from bs4 import BeautifulSoup
import requests
import random

# clear screen


def clear():
    os.system("cls" if os.name == "nt" else "clear")


clear()

# print ascii art in red
print(
    """\033[91m 
  /$$$$$$                                                   /$$      /$$          
 /$$__  $$                                                 | $$$    /$$$          
| $$  \__/  /$$$$$$$  /$$$$$$  /$$$$$$   /$$$$$$   /$$$$$$ | $$$$  /$$$$  /$$$$$$ 
|  $$$$$$  /$$_____/ /$$__  $$|____  $$ /$$__  $$ /$$__  $$| $$ $$/$$ $$ /$$__  $$
 \____  $$| $$      | $$  \__/ /$$$$$$$| $$  \ $$| $$$$$$$$| $$  $$$| $$| $$$$$$$$
 /$$  \ $$| $$      | $$      /$$__  $$| $$  | $$| $$_____/| $$\  $ | $$| $$_____/
|  $$$$$$/|  $$$$$$$| $$     |  $$$$$$$| $$$$$$$/|  $$$$$$$| $$ \/  | $$|  $$$$$$$
 \______/  \_______/|__/      \_______/| $$____/  \_______/|__/     |__/ \_______/
                                       | $$                                       
                                       | $$                                       
                                       |__/                                       

    \033[0m"""
)


webInput = input("Enter a website: ")

# if website is invalid print error in red, continue
if re.match(r"^(?:http|ftp)s?://", webInput) == None:
    print("\033[91m" + "Invalid website! (put http:// or https:// in front of the URL)" + "\033[0m")
    input("Press any key to continue...")
    exit()

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
headers = {"User-Agent": user_agent}


def ping(webInput):
    try:
        response = urllib.request.urlopen(webInput)
        print("\033[94m" + webInput + " is up!")
        return True
    except urllib.request.URLError as e:
        # fake a useragent
        print("\033[94m" + webInput + " is down, invalid, or errored in another way!")
        return False


if ping(webInput):
    print("\033[93m" + "-" * len(webInput) + "\033[0m")

    # download raw HTML
    def get_html(webInput):
        try:
            r = requests.get(webInput, headers=headers)
            html = r.text
            html = html.encode("ascii", "ignore").decode("utf-8", "ignore")
            return html
        except requests.exceptions.ConnectionError:
            return False

    rawText = get_html(webInput)

    # create email regex
    emailRegex = re.compile(r"[\w\.-]+@[\w\.-]+")
    emails = re.findall(emailRegex, rawText)
    print("Possible emails found: " + "\033[1;31;40m" + str(emails) + "\033[0;37;40m")

    # get links
    def get_links(rawText):
        soup = BeautifulSoup(rawText, "html.parser")
        return [link.get("href") for link in soup.find_all("a") if link.get("href") is not None]

    print("Amount of links found: " + "\033[1;31;40m" + str(len(get_links(rawText))) + "\033[0;37;40m")

    # make regex for phones
    phoneRegex = re.compile(r"\d\d\d-\d\d\d-\d\d\d\d")
    phoneMatches = phoneRegex.findall(rawText)
    print("Possible phone numbers found: " + "\033[92m" + str(phoneMatches) + "\033[0m")

    # download names.txt
    if not os.path.exists("names.txt"):
        urllib.request.urlretrieve(
            "https://www.usna.edu/Users/cs/roche/courses/s15si335/proj1/files.php%3Ff=names.txt&downloadcode=yes",
            "names.txt",
        )

    # find names
    with open("names.txt", "r") as f:
        names = f.readlines()
    names = [x.strip() for x in names]
    nameMatches = [name for name in names if name in rawText]
    print("Possible names found: " + "\033[1;31;40m" + str(len(nameMatches)) + "\033[0;37;40m")

    def write_to_file(data, file_name):
        random_name = str(random.randint(1, 999999999)) + file_name
        with open(random_name, "w") as text_file:
            if data != None:
                for item in data:
                    text_file.write(item + "\n")
        return random_name

    write_to_file(get_links(rawText), "links.txt")
    write_to_file(phoneMatches, "phones.txt")
    write_to_file(emails, "emails.txt")
    write_to_file(rawText, "raw.txt")
    write_to_file(nameMatches, "names.txt")

    input("\033[95m" + "Finished! Exported all data to their respective text files. Press enter to exit..." + "\033[0m")

else:
    input("\033[91m" + "Press enter to exit..." + "\033[0m")
    exit()
