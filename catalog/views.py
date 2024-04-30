from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q

from django.contrib import messages

from django.urls import reverse_lazy

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

from .forms import RenewBookForm

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


class BookDetailView(SuccessMessageMixin, generic.DetailView):
    model = Book

    # permission_required = 'catalog.delete'
    info_message = "Вы можете взять эту книгу в аренду."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book_views'] = self.request.session[f"book_{self.kwargs['pk']}_viewed"]
        return context

    def get(self, request, *args, **kwargs):
        book_id = self.kwargs['pk']
        book_views_times = request.session.get(f'book_{book_id}_viewed', 0)
        request.session[f'book_{book_id}_viewed'] = book_views_times + 1
        messages.info(self.request, self.info_message)
        return super().get(request, *args, **kwargs)




class AuthorDetailView(generic.DetailView):
    model = Author

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
    paginate_by = 10


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


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    book_inst = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst': book_inst})


class AuthorCreate(SuccessMessageMixin, CreateView):
    model = Author
    fields = '__all__'
    initial={'date_of_death': '12/10/2016'}

    success_message = "Автор успешно добавлен."

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response


class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')


def searching(request):
    if request.method == "POST":
        # print(request.POST)
        searched = request.POST.get('searched').title()
        books_results = Book.objects.filter(title__icontains=searched)
        authors_results = Author.objects.filter(Q(first_name__icontains=searched) | Q(last_name__icontains=searched))
        return render(request, "catalog/search_page.html", {'searched': searched,
                                                            'books_results': books_results,
                                                            'authors_results': authors_results})
    else:
        return render(request, "catalog/search_page.html")
