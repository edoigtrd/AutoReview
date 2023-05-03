import subprocess
import uuid
import os
import openai
import config
import json
import bs4 as bs
import requests
import json
import time
from deep_translator import GoogleTranslator
from langdetect import detect
import tarfile
import datetime

id = uuid.uuid4()
id = str(id).replace("-", "")

os.mkdir(id)

if os.name == "nt":
    editor = "notepad"
else:
    editor = "vim"
    if os.getenv("EDITOR"):
        editor = os.getenv("EDITOR")

openai.api_key = config.config.keys.openai

# get the presentation from GPT-3 using the prompt
def get_presentation(prompt) :
    with open("prompt.txt", "r") as f:
        prompt = f.read().format(prompt)

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["</body>"]
    )
    return "#"+response.choices[0].text

# This was initially used to generate html from a markdown document but it was not working well
def get_doc(prompt) :
    response = openai.Edit.create(
        model="code-davinci-edit-001",
        input=prompt,
        instruction="Using webslides and tailwind css, convert this to a html presentation",
        temperature=0.7,
        top_p=1,
        stop=["</body>"]
    )
    return response.choices[0].text

# generate images from the document using deepai stable diffusion api
def generate_images(doc) :
    d = ""
    with open(doc, "r") as f:
        d = f.read()
    soup = bs.BeautifulSoup(d, "html.parser")
    # get all images in the document
    images = soup.find_all("img")
    parent_dir = os.path.dirname(os.path.abspath(doc))
    for image in images:
        src = image["src"]
        prompt = image["prompt"]
        if detect(prompt) != "en":
            prompt = GoogleTranslator(source='auto', target='en').translate(prompt)
        print(src, prompt)
        r = requests.post(
            "https://api.deepai.org/api/stable-diffusion",
            data={
                'text': prompt,
            },
            headers={'api-key': config.config.keys.deepai}
        )
        response = r.json()
        print(response)
        iurl = response["output_url"]
        # download the image names as the src in the document folder
        r = requests.get(iurl, allow_redirects=True)
        if not src.startswith("/"):
            src = f"/{src}"
        # check if path exists, if no create every folders
        adir = os.path.dirname(f"{parent_dir}{src}")
        if not os.path.exists(adir):
            os.makedirs(adir)
        open(f"{parent_dir}{src}", 'wb').write(r.content)


with open(f"{id}/prompt.txt", "w") as f:
    f.write("")

subprocess.run([editor, f"{id}/prompt.txt"])

with open(f"{id}/prompt.txt", "r") as f:
    prompt = f.read()

prompt = "\n".join([line for line in prompt.splitlines() if not line.startswith("#")]).strip()

print("Generating presentation...")
pres = get_presentation(prompt)


# unzip template.tgz to the id folder
with tarfile.open("template.tgz", "r:gz") as tar:
    tar.extractall(id)

# wait for the files to be copied
while not os.path.exists(f"{id}/template/pres.html"):
    time.sleep(0.1)

c = ""
doc = ""

with open(f"{id}/template/pres.html", "r") as f:
    c = f.read()
    doc = c.replace("{body}", str(pres))

with open(f"{id}/template/pres.html", "w") as f:
    f.write(doc)

print("Generating images...")
generate_images(f"{id}/template/pres.html")

# rename id folder to the current date ISO8601 format
os.rename(id, datetime.datetime.now().isoformat())

id = datetime.datetime.now().isoformat()

print("="*os.get_terminal_size().columns)
print(f"You can poen your file {os.path.abspath(id)}/template/pres.html in your browser")
print("="*os.get_terminal_size().columns)

if os.name == "nt":
    os.system(f"start {id}/template/pres.html")
else:
    os.system(f"xdg-open {id}/template/pres.html")
