from mrjob.job import MRJob
import string
from nltk import ngrams

class MRGrams(MRJob):

    def mapper(self, _, line):
        n = 2
        line_new = line.translate(str.maketrans('', '', string.punctuation))
        numerals_removal = ''.join([i for i in line_new if not i.isdigit()]).split()
        grams = [numerals_removal[i:i+n] for i in range(len(numerals_removal)-n+1)]
        
        for gram in grams:
            yield gram, 1

    def combiner(self, key, values):
        yield key, sum(values)

    def reducer(self, key, values):
        yield key, sum(values)


if __name__ == '__main__':
    MRGrams.run()
