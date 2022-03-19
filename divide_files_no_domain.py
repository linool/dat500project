import subprocess
import urllib.request
from urllib.parse import urlparse
from os import path


with open("filenames_no_domain") as file:
    line_list = []
    for line in file:
        line = line.strip()
        tmp = line.split('/')
        if  tmp[4] == 'crawldiagnostics' or tmp[4] == 'robotstxt':
            continue
        else:
            line_list.append(line)
    # number of files to divide to
    n = 4
    l = len(line_list)//n

    for i in range(n):
        file_name = str(i) + "_filenames_no_domain"
        with open(file_name, "w+") as w:
            if i == n -1:
                w.write('\n'.join(line_list[i*l:]))
            else:
                w.write('\n'.join(line_list[i*l:(i+1)*l]))

