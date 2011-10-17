'''
Created on 17.10.2011

@author: xaralis
'''
# -*- coding: utf-8 -*-
from django.http import HttpResponsePermanentRedirect

from ella.core.views import ObjectDetail

class ArticleDetail(ObjectDetail):
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
    def __call__(self, request, context, page):
        if int(page) == 1:
            return HttpResponsePermanentRedirect(context['object'].get_absolute_url())
        
        return self.render_page(request, context, int(page))

article_page = ArticlePage()
