from mrjob.job import MRJob
from urllib.parse import urlparse
import string

def remove_punctuation(line):
    tmp = ''
    for ch in line:
        if ch not in string.punctuation:
            tmp = tmp + ch
        else: 
            tmp = tmp + ' '
    return tmp

class MRDomainWords(MRJob):
    def mapper_init(self):
        self.topdomain = ''
        self.in_body = False
        self.body = []

    def mapper(self, _, line):
        if line.strip() == 'WARC/1.0':
            self.in_body = False
        elif line.find('WARC-Target-URI:') == 0:
            if not self.in_body:
                page_uri = line[17:].strip()
                link = urlparse(page_uri)
                domain = link.hostname
                if domain:
                    tmp = domain.split(".")
                    self.topdomain = tmp[-2]+"."+tmp[-1]
        elif line.strip() == '':
            if not self.in_body:
                self.in_body = True
            else:
                text = ' '.join(self.body)
                text = remove_punctuation(text)
                total = len(text.split())
                yield self.topdomain, total
                self.in_body = False
                self.topdomain = ''
                self.body = []

        if self.in_body:
            self.body.append(line)

    def combiner(self, key, values):
        yield key, sum(values)

    def reducer(self, key, values):
        yield key, sum(values)

if __name__ == '__main__':
    MRDomainWords.run()
