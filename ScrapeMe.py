import re
import subprocess
import urllib.request
import os
from bs4 import BeautifulSoup
import requests
import codecs
import random

# clear screen 
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
clear()

# print ascii art in red
def print_red(text):
    print("\033[91m" + text + "\033[0m")
print_red("""
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

    """)

# ask for user input
webInput = input("Enter a website: ")
# if website is invalid print error in red, continue
if re.match(r'^(?:http|ftp)s?://', webInput) == None:
    print("\033[91m" + "Invalid website! (put http:// or https:// in front of the URL)" + "\033[0m")
    input("Press any key to continue...")
    exit()

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
headers = {'User-Agent': user_agent}
# ping website 
def ping(webInput):
    try:
        response = urllib.request.urlopen(webInput)
        print("\033[94m" + webInput + " is up!")
        return True
    except urllib.request.URLError as e:
        # fake a useragent
        print("\033[94m" + webInput + " is down, invalid, or errored in another way!")
        return False

# if website returns ping, then continue
if ping(webInput):
    print("\033[93m" + "-" * len(webInput) + "\033[0m")
    
    # download raw HTML
    def get_html(webInput):
        try:
            r = requests.get(webInput, headers=headers)
            html = r.text
            html = html.encode('ascii', 'ignore').decode('utf-8', 'ignore')
            return html
        except requests.exceptions.ConnectionError:
            return False
    rawText = get_html(webInput)

    # write raw HTML to file
    def write_html(rawText):
        randomName = str(random.randint(1, 999999999)) + "rawHTML.txt"
        # write raw HTML to text file
        with open(randomName, "w") as text_file:
            text_file.write(rawText)
        return randomName
    write_html(rawText)
    

    # create email regex, find emails in text, print in red.
    emailRegex = re.compile(r'[\w\.-]+@[\w\.-]+')
    emails = re.findall(emailRegex, rawText)
    print("Possible emails found: " + "\033[1;31;40m" + str(emails) + "\033[0;37;40m")
    # write emails to file with random name
    def write_emails(emails):
        randomName = str(random.randint(1, 999999999)) + "emails.txt"
        with open(randomName, "w") as text_file:
            text_file.write(str(emails))
        return randomName
    # run write_emails function
    write_emails(emails)


    # Scan website for links using BeautifulSoup
    def get_links(rawText):
        soup = BeautifulSoup(rawText, 'html.parser')
        links = []
        for link in soup.find_all('a'):
            links.append(link.get('href'))
        links = [x for x in links if x is not None]
        return links

    # print amount of links found
    print("Amount of links found: " + "\033[1;31;40m" + str(len(get_links(rawText))) + "\033[0;37;40m")

    # write links to file with random name
    def write_links(links):
        randomName = str(random.randint(1, 999999999)) + "links.txt"
        with open(randomName, "w") as text_file:
            if links != None:
                for link in links:
                    text_file.write(link + "\n")
        return randomName
    # run write_links function
    write_links(get_links(rawText))


    # make regex for phone finding, check if in text, print in green
    phoneRegex = re.compile(r'\d\d\d-\d\d\d-\d\d\d\d')
    phoneMatches = phoneRegex.findall(rawText)
    print("Possible phone numbers found: " + "\033[92m" + str(phoneMatches) + "\033[0m")

    # write phone numbers to file with random name, separated by newline
    def write_phones(phoneMatches):
        randomName = str(random.randint(1, 999999999)) + "phones.txt"
        with open(randomName, "w") as text_file:
            if phoneMatches != None:
                for phone in phoneMatches:
                    text_file.write(phone + "\n")
        return randomName
    # run write_phones function
    write_phones(phoneMatches)

    # download names.txt if it doesnt already exist
    if not os.path.exists("names.txt"):
        urllib.request.urlretrieve("https://www.usna.edu/Users/cs/roche/courses/s15si335/proj1/files.php%3Ff=names.txt&downloadcode=yes", "names.txt")
        

    # open names.txt, read and check if any words from names.txt are in rawText and append to list, exclude spaces
    with open("names.txt", "r") as f:
        names = f.readlines()
    names = [x.strip() for x in names]
    nameMatches = []
    for name in names:
        if name in rawText:
            nameMatches.append(name)
    # Count names in nameMatches and print amount in red
    print("Possible names found: " + "\033[1;31;40m" + str(len(nameMatches)) + "\033[0;37;40m")

    # write names to file with random name, make each name on new line
    def write_names(nameMatches):
        randomName = str(random.randint(1, 999999999)) + "names.txt"
        with open(randomName, "w") as text_file:
            if nameMatches != None:
                for name in nameMatches:
                    text_file.write(name + "\n")
        return randomName
    # run write_names function
    write_names(nameMatches)


    input("\033[95m" + "Finished! Exported all data to their respective text files. Press enter to exit..." + "\033[0m")

else:
    input("\033[91m" + "Press enter to exit..." + "\033[0m")
    exit()
    