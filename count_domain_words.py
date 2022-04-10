from mrjob.job import MRJob
from urllib.parse import urlparse

class MRMultilineInput(MRJob):               
    def mapper_init(self):
        self.topdomain = ''
        self.in_body = False
        self.body = []
    
    def mapper(self, _, line):
        if line.find('WARC-Target-URI:') == 0:
            page_uri = line[17:].strip()
            link = urlparse(page_uri)
            domain = link.hostname
            if domain:
                tmp = domain.split(".")
                self.topdomain = tmp[-2]+"."+tmp[-1]
            
        if self.in_body:
            self.body.append(line)
        
        if line.find('Content-Length:') == 0 and not self.in_body:
            self.in_body = True
        
        if line.find('WARC/1.0') == 0 and self.in_body:
            text = ''.join(self.body)
            total = len(text.split())
            yield self.topdomain, total
            self.in_body = False
            self.topdomain = ''
            self.body = []    
            
    def combiner(self, key, values):
        yield key, sum(values)

    def reducer(self, key, values):
        yield key, sum(values)
                       
if __name__ == '__main__':
    MRMultilineInput.run()
