from django.views import generic
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage

from .models import Book, Author, BookInstance, Genre


def index(request):
    """
        Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Доступные книги (статус = 'a')

    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()  # Метод 'all()' применён по умолчанию.

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    context = {'num_books': num_books,
               'num_instances': num_instances,
               'num_instances_available': num_instances_available,
               'num_authors': num_authors}

    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    # context_object_name = 'my_book_list'
    #
    # template_name = 'new_template.html'
    #
    # def get_queryset(self):
    #     return Book.objects.all()
    #
    # def get_context_data(self, **kwargs):
    #     # В первую очередь получаем базовую реализацию контекста
    #     context = super(BookListView, self).get_context_data(**kwargs)
    #     # Добавляем новую переменную к контексту и инициализируем её некоторым значением
    #     context['some_data'] = 'This is just some data'
    #     return context

    paginate_by = 2


class BookDetailView(generic.DetailView):
    model = Book

# def book_detail_view(request, pk):
#     try:
#         book_id = Book.objects.get(pk=pk)
#     except Book.DoesNotExist:
#         raise Http404("Book does not exist")
#
#     #book_id=get_object_or_404(Book, pk=pk)
#
#     return render(request, 'catalog/book_detail.html', context={'book': book_id})


# def author_list_page_view(request, page=1):
#     authors_list = Author.objects.all()
#
#     paginator = Paginator(authors_list, 2)  # 2 users per page
#
#     # We don't need to handle the case where the `page` parameter
#     # is not an integer because our URL only accepts integers
#     try:
#         page_obj = paginator.page(page)
#     except EmptyPage:
#         # if we exceed the page limit we return the last page
#         page_obj = paginator.page(paginator.num_pages)
#
#     context = {
#         'page_obj': page_obj,
#     }
#
#     return render(request, 'catalog/author_list.html', context=context)

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 2
