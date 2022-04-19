from mrjob.job import MRJob
from urllib.parse import urlparse
import string

trailing_punctuation = '!,.;?'

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

def is_ngrams(x,n):
    for i in range(n-1):
        if x[i][-1] in trailing_punctuation:
            return False
        if x[i][0].isdigit():
            return False
    if x[n-1][0].isdigit():
        return False
    for i in range(n):
        if x[i][0] in string.punctuation:
            return False
    return True

def remove_trailing_punctuation(x, n):
    word = x[-1]
    if word[-1] in trailing_punctuation:
        word = word[:-1]
        if word and word[-1] == '.':
                word = word[:-1]
                if word and word[-1] == '.':
                    word = word[:-1]
                    if word and word[-1] == '.':
                        word = word[:-1]
    x[-1] = word
    return x
    
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
                if len(self.body)>0:
                    for text in self.body:
                        text = text.lower()
                        words = text.split()
                        # generate n-grams
                        n = 2
                        xgrams = n_grams(words, n)
                        for x in xgrams:
                            if is_ngrams(x,n):
                                x = remove_trailing_punctuation(x,n)
                                if x and x[0]: 
                                    yield x, 1
                self.in_body = False
                self.topdomain = ''
                self.body = []

        if self.in_body:
            if self.topdomain == 'uio.no':
                self.body.append(line)

    def combiner(self, key, values):
        yield key, sum(values)

    def reducer(self, key, values):
        yield key, sum(values)

if __name__ == '__main__':
    MRMultilineInput.run()
