import os
import requests
from zipfile import ZipFile


release_url = r'https://github.com/d3-worgan/edfbrowser/releases/download/v1.0/edfbrowser_1.zip'
print(os.getcwd())
save_path = os.path.join(os.getcwd(), 'edfbrowser.zip')
print(save_path)
if os.path.exists(save_path):
    os.remove(save_path)
r = requests.get(release_url, stream=True)
with open(save_path, 'wb') as f:
    for chunk in r.iter_content(chunk_size=128):
        f.write(chunk)
with ZipFile(save_path, 'r') as z:
    z.extractall()
