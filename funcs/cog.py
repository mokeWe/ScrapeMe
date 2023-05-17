import os
import random
import re
import urllib.request


def download_images(img_urls, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

    images = []
    for img_url in img_urls:
        try:
            filename = os.path.basename(img_url)
            filepath = os.path.join(folder, filename)
            urllib.request.urlretrieve(img_url, filepath)
            print(f"Downloaded: {img_url}")
            images.append(filepath)
        except Exception as e:
            print(f"Failed to save image: {e}")
    print("Recieved images")
    return images


def get_phones(text_with_contact_info):
    phone_regex = re.compile(r"((\s|-|\.)?(\d{3})(\s|-|\.)?(\d{4}))")
    return phone_regex.findall(text_with_contact_info)


def get_emails(text_with_contact_info):
    email_regex = re.compile(r"\w+[\w.]*\w+@\w+[\w.]*\w+")
    return email_regex.findall(text_with_contact_info)


def write_to_file(data, file_name):
    random_name = f"{random.randint(1, 100)}_{file_name}"
    results_dir = "results"

    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    try:
        with open(os.path.join(results_dir, random_name), "w") as text_file:
            if data is not None:
                for item in data:
                    text_file.write(f"{item}\n")
    except Exception as e:
        print(f"Failed to write to file: {e}")
        return None

    return random_name
