from mrjob.job import MRJob
import json
from urllib.parse import urlparse

class MRCountSum(MRJob):

    def mapper(self, _, line):
        line = line.strip()
        try:
            page_dict = json.loads(line[line.find('{"url":'):])
            charset = page_dict["charset"]
            if charset:
                yield charset, 1
        except:
            yield "error", 1

    def combiner(self, key, values):
        yield key, sum(values)

    def reducer(self, key, values):
        yield key, sum(values)


if __name__ == '__main__':
    MRCountSum.run()
