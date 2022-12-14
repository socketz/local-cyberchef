from io import BytesIO
from requests import Session
import json
import zipfile
from pathlib import Path

latest_version = "https://github.com/gchq/CyberChef/releases/latest"
api_latest = "https://api.github.com/repos/gchq/CyberChef/releases/latest"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
    "Accept": "application/vnd.github.v3+json"
}

sess = Session()
sess.headers.update(headers)

res = sess.get(api_latest)
if res.ok:
    parsed = json.loads(res.text)
    zip_name = parsed['assets'][0]['name']
    zip_url = parsed['assets'][0]['browser_download_url']
    print("Downloading URL file: ", zip_url)
    zip_res = sess.get(zip_url, allow_redirects=True)

    bio = BytesIO(zip_res.content)

    # Extracting zip file in-memory
    zipf = zipfile.ZipFile(bio)
    zipf.extractall()

    # Remove all .txt files
    txt_files = Path('.').glob('**/*.txt')
    for txt_f in txt_files:
        txt_f.unlink()

    # Remove and rename new html file
    print("Renaming files...")
    Path('CyberChef.html').unlink(missing_ok=True)
    for html_f in Path('.').glob('*.html'):
        html_f.rename('CyberChef.html')

    print("Done!")
