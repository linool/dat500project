from urllib.parse import urlparse
import urllib.request
from os import path
import json
import subprocess

with open("cc-index.paths") as index_paths_file:
    for line in index_paths_file:
        line = line.strip()
        index_file_name = line.split('/')[-1]
        if not path.exists(index_file_name):
            url = 'https://commoncrawl.s3.amazonaws.com/' + line
            urllib.request.urlretrieve(url, index_file_name)
        if index_file_name[-3:] == '.gz':
            subprocess.run('gunzip '+index_file_name,shell=True)
            index_file_name = index_file_name[:-3]
        with open(index_file_name) as file, open('pages_domain_no.txt','a') as w:
            for page in file:
                if page[:3] == 'no,':
                    w.write(page)
