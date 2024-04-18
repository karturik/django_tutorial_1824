from .views import *
from django.urls import path, re_path


urlpatterns = [
    path('', index, name='index'),
    re_path(r'^books/$', BookListView.as_view(), name='books'),
    re_path(r'^book/(?P<pk>\d+)$', BookDetailView.as_view(), name='book-detail'),
    re_path(r'^author/(?P<pk>\d+)$', AuthorDetailView.as_view(), name='author-detail'),

    path('authors/', AuthorListView.as_view(), name='authors'),

    re_path(r'^mybooks/$', LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    re_path(r'^allborrowed/$', LoanedBooksByAllListView.as_view(), name='all-borrowed'),

    re_path(r'^book/(?P<pk>[-\w]+)/renew/$', renew_book_librarian, name='renew-book-librarian'),

    re_path(r'^author/create/$', AuthorCreate.as_view(), name='author_create'),
    re_path(r'^author/(?P<pk>\d+)/update/$', AuthorUpdate.as_view(), name='author_update'),
    re_path(r'^author/(?P<pk>\d+)/delete/$', AuthorDelete.as_view(), name='author_delete'),


]
