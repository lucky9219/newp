from haystack import indexes

from .models import *


class NewsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    content_auto=indexes.EdgeNgramField(model_attr='title')   
  

    def get_model(self):
        return user_news

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

