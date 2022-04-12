from os import remove
from mrjob.job import MRJob
from nltk import ngrams
import string

def is_header(line):
    if line.find('WARC/1.0') == 0:
        return True
    elif line.find('WARC-Type:') == 0:
        return True
    elif line.find('WARC-Target-URI:') == 0:
        return True
    elif line.find('WARC-Date:') == 0:
        return True
    elif line.find('WARC-Record-ID:') == 0:
        return True
    elif line.find('WARC-Refers-To:') == 0:
        return True
    elif line.find('WARC-Block-Digest:') == 0:
        return True
    elif line.find('WARC-Identified-Content-Language:') == 0:
        return True
    elif line.find('Content-Type:') == 0:
        return True
    elif line.find('Content-Length:') == 0:
        return True
    else: 
        return False
def remove_punctuation(line):
    tmp = ''
    for ch in line:
        if ch not in string.punctuation:
            tmp = tmp + ch
    return tmp

class MRCountSum(MRJob):
    def mapper(self, _, line):
        if not is_header(line):
            str = remove_punctuation(line)
            n = 1
            xgrams = ngrams(str.split(), n)
            for x in xgrams:
                yield x, 1

    def combiner(self, key, values):
        yield key, sum(values)

    def reducer(self, key, values):
        yield key, sum(values)


if __name__ == '__main__':
    MRCountSum.run()
