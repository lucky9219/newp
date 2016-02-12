from haystack import indexes

from .models import news


class NewsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    content_auto=indexes.EdgeNgramField(model_attr='title')   
  

    def get_model(self):
        return news

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()