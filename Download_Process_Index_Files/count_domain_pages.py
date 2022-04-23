from mrjob.job import MRJob
import json
from urllib.parse import urlparse

class MRCountSum(MRJob):

    def mapper(self, _, line):
        line = line.strip()
        try:
            page_dict = json.loads(line[line.find('{"url":'):])
            link = urlparse(page_dict["url"])
            domain = link.hostname
            if domain:
                if page_dict["mime-detected"] == "text/html":
                    tmp = domain.split(".")
                    domain = tmp[-2]+"."+tmp[-1]
                    yield domain, 1
        except:
            yield "error", 1

    def combiner(self, key, values):
        yield key, sum(values)

    def reducer(self, key, values):
        yield key, sum(values)


if __name__ == '__main__':
    MRCountSum.run()
