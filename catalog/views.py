from django.views import generic
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator, EmptyPage

from .models import Book, Author, BookInstance, Genre


@login_required
# @permission_required('catalog.can_edit')
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

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # if request.user.is_authenticated:
    #     ...
    # else:
    #     ...

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    context = {'num_books': num_books,
               'num_instances': num_instances,
               'num_instances_available': num_instances_available,
               'num_authors': num_authors,
               'num_visits': num_visits}

    return render(request, 'index.html', context=context)


class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

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

    paginate_by = 10


class BookDetailView(PermissionRequiredMixin, generic.DetailView):
    model = Book

    # permission_required = 'catalog.delete'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book_views'] = self.request.session[f"book_{self.kwargs['pk']}_viewed"]
        return context

    def get(self, request, *args, **kwargs):
        book_id = self.kwargs['pk']
        book_views_times = request.session.get(f'book_{book_id}_viewed', 0)
        request.session[f'book_{book_id}_viewed'] = book_views_times + 1
        return super().get(request, *args, **kwargs)

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


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class LoanedBooksByAllListView(PermissionRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    permission_required = 'catalog.can_mark_returned'

    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')
