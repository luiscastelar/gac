import re 

class HtmlTokenizer():
    tokens = []

    def parse(self, html):
        self.tokens = re.findall("<_*(\w*)", str(html))
        #print(self.tokens)
        

