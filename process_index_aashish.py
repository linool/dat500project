from urllib.parse import urlparse
import urllib.request
import gzip
import json
BLOCKSIZE = 10000000
with open("cc-index.paths") as index_paths_file:
    lines = index_paths_file.readlines()
    for line in lines:
        line = line.strip()
        index_file_name = line.split('/')[-1]
        url = 'https://commoncrawl.s3.amazonaws.com/' + line
        #urllib.request.urlretrieve(url, index_file_name)
        with gzip.open(index_file_name, 'rt') as f:
            pages = f.readlines(BLOCKSIZE)
            while pages:
                pages_no_domain = []
                for idx, page in enumerate(pages):
                    #print(page)
                    #break
                    try:
                        page_dict = json.loads(page[page.find("{"):])
                    except:
                        continue
                    link = urlparse(page_dict["url"])
                    domain = link.hostname
                    if domain[-3:] == ".ar":
                        pages_no_domain.append(page)
                    #print("Page Encountered: ", idx)
                #break
                with open('pages_domain_no.txt','a') as w:
                    for page_no in pages_no_domain:
                        w.write(page_no+'\n')
