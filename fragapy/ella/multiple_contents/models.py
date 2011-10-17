'''
Created on 17.10.2011

@author: xaralis
'''
from ella.articles.models import Article

CONTENT_SPLIT_MARKER = '<!--PB-->'

def get_contents(self):
    if not hasattr(self, '__split_contents'):
        if self.content is not None:
            self.__split_contents = self.content.content.split(CONTENT_SPLIT_MARKER)
        else:
            return None
    return self.__split_contents

def get_content_count(self):
    contents = self.get_contents()
    if contents is not None:
        return len(contents)
    return 0

def get_content(self, index):
    if self.get_content_count() >= 1:
        return self.get_contents()[index]
    
Article.get_contents = get_contents
Article.get_content_count = get_content_count
Article.get_content = get_content