'''
Created on 17.10.2011

@author: xaralis
'''
from django.http import HttpResponsePermanentRedirect

from ella.core.views import ObjectDetail

class ArticleDetail(ObjectDetail):
    """
    Article detail that adds possibility to show splitted contents. Shows 
    first page/first content available. Adds following variables to template context:
    
        `content`             current content to show
        `content_list`        list of marked-up contents available for the article
        `content_index`       index of current contnt
        `content_count`       total number of available contents
        `next_content_index`  next content index or None if this is the last content
        `prev_content_index`  previous content index or None if this is the first content
        `has_next_content`    True if this isn't the last content
        `has_prev_content`    True if this isn't the first content
        `has_some_content`    True if some content is available
    """
    
    def prepare_content_context(self, article, page):
        content_count = article.get_content_count()
        return {
            'content': article.get_content(page - 1),
            'content_list': article.get_contents(),
            'content_index': page,
            'content_count': content_count,
            'next_content_index': page + 1 if page + 1 <= content_count else None,
            'prev_content_index': page - 1 if page - 1 > 0 else None, 
            'has_next_content': content_count > page,
            'has_prev_content': page > 1,
            'has_some_content': content_count != 0,
        }
        
    def render_page(self, request, context, page):
        article = context['object']
        context.update(self.prepare_content_context(article, page))
        return self.render(request, context, self.get_templates(context))
        
    def __call__(self, request, context):
        return self.render_page(request, context, 1)

article_detail = ArticleDetail()

class ArticlePage(ArticleDetail):
    """
    Handles browsing of given article page. Populates template context
    by same variables as ArticleDetail.
    
    When first page is requested, permanent redirect is made to the 
    base page -> ArticleDetail. 
    """
    def __call__(self, request, context, page):
        if int(page) == 1:
            return HttpResponsePermanentRedirect(context['object'].get_absolute_url())
        
        return self.render_page(request, context, int(page))

article_page = ArticlePage()
