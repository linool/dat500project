from mrjob.job import MRJob
from urllib.parse import urlparse
import string

def n_grams(words_list, n):
    ngrams_list = []
    if n > len(words_list):
        return ngrams_list
    for i in range(len(words_list)-n+1):
        tmp = ['']*n
        for j in range(n):
            tmp[j] = words_list[i+j]
        ngrams_list.append(tmp)
    return ngrams_list

def remove_punctuation(line):
    tmp = ''
    for ch in line:
        if ch not in string.punctuation:
            tmp = tmp + ch
        else: 
            tmp = tmp + ' '
    return tmp

class MRMultilineInput(MRJob):
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
                words = text.split()
                # generate n-grams
                n = 2
                xgrams = n_grams(words, n)
                for x in xgrams:
                    yield x, 1
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
    MRMultilineInput.run()
