from .views import *
from django.urls import path, re_path


urlpatterns = [
    path('', index, name='index'),
    re_path(r'^books/$', BookListView.as_view(), name='books'),
    re_path(r'^book/(?P<pk>\d+)$', BookDetailView.as_view(), name='book-detail'),

    path('authors/', AuthorListView.as_view(), name='authors'),

]
