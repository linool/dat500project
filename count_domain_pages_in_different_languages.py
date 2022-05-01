from mrjob.job import MRJob
import json
from urllib.parse import urlparse

class MRCountSum(MRJob):

    def mapper(self, _, line):
        line = line.strip()
        try:
            page_dict = json.loads(line[line.find('{"url":'):])
            lan = page_dict["languages"]
            if lan:
                if page_dict["mime-detected"] == "text/html":
                    if lan.find(',') == -1:
                        yield lan, 1
                        yield "in_total", 1
                    else:
                        yield "mixed_languages", 1
                        yield "in_total", 1
                        if lan.find('nor') != -1:
                            yield "nor_in_mixed", 1
                        if lan.find('eng') != -1:
                            yield "eng_in_mixed", 1
                        if lan.find('nno') != -1:
                            yield "nno_in_mixed", 1
        except:
            yield "error", 1

    def combiner(self, key, values):
        yield key, sum(values)

    def reducer(self, key, values):
        yield key, sum(values)


if __name__ == '__main__':
    MRCountSum.run()
