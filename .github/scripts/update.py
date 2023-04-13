from datetime import datetime
from os.path import dirname, join


from bs4 import BeautifulSoup
from git import Repo
import requests

URL = 'https://www.ianbakst.com'


if __name__ == '__main__':
    r = requests.get(URL)
    s = BeautifulSoup(r.text, 'html.parser')
    texts = s.get_text()
    longest = 0
    bio = ''
    for text in texts.split('\n\n\n\n'):
        if len(text) > longest:
            bio = text
            longest = len(text)
    with open(join(dirname(__file__), 'base-readme.md'), 'r') as f:
        base = f.read()

    full_readme = base + "\n" + "### Bio \n\n" + bio

    with open('./README.md', 'w') as f:
        f.write(full_readme)
    now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    repo = Repo('.')
    repo.git.add(update=True)
    repo.index.commit(f'Updated README.md {now}')
    repo.remote(name='origin').push()
