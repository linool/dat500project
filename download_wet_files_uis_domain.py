import subprocess
import urllib.request
from urllib.parse import urlparse
from os import path


with open("filenames_uis_no.txt") as file:
    for line in file:
        line = line.strip()
        line = line.replace(".warc.", ".warc.wet.")
        tmp = line.split('/')
        if  tmp[4] == 'crawldiagnostics' or tmp[4] == 'robotstxt':
            continue
        else:
            line = line.replace("/warc/", "/wet/")
            print(line)
            file_name = tmp[-1]
            if not path.exists(file_name):
                url = 'https://commoncrawl.s3.amazonaws.com/' + line
                try:
                    urllib.request.urlretrieve(url, file_name)
                except:
                    print("Couldn't download file "+url)
            if path.exists(file_name):
                subprocess.run('gunzip '+file_name,shell=True)
                file_name = file_name[:-3]
                with open(file_name, encoding="utf-8") as f:
                    is_no_domain = False
                    line_list = []
                    for f_line in f:
                        f_line = f_line.strip()
                        if f_line[:8] == 'WARC/1.0':
                            if is_no_domain:
                                with open('extracted_from_wet_files_uis.txt','a',encoding="utf-8") as w:
                                    w.write('\n'.join(line_list))
                            line_list = []
                            line_list.append(f_line)
                            is_no_domain = False
                        elif f_line[:16] == 'WARC-Target-URI:':
                            link = urlparse(f_line[17:])
                            domain = link.netloc
                            if domain:
                                if domain[-7:] == '.uis.no' or domain[-7:] == '/uis.no':
                                    is_no_domain = True
                            line_list.append(f_line)
                        else:
                            line_list.append(f_line)
                subprocess.run('rm '+file_name,shell=True)