import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy

from .forms import RenewBookForm
from .models import Book, Author, BookInstance, Genre
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


# Create your views here.
def index(request):
    num_books = Book.objects.all().count()
    num_author = Author.objects.all().count()

    num_instance = BookInstance.objects.all().count()
    num_instance_available = BookInstance.objects.filter(status__exact='a').count()

    num_book_black = Book.objects.filter(title__icontains='black').count()

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_authors': num_author,
        'num_instances': num_instance,
        'num_instances_available': num_instance_available,
        'num_books_black': num_book_black,
        'num_visits': num_visits
    }

    return render(request, 'catalog/index.html', context)


class BookListView(ListView):
    model = Book
    paginate_by = 3


class BookDetailView(DetailView):
    model = Book


class AuthorListView(ListView):
    model = Author
    paginate_by = 10


class AuthorDetailView(DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class BorrowedListView(PermissionRequiredMixin, ListView):
    permission_required = 'catalog.can_mark_return'
    model = BookInstance
    template_name = 'catalog/borrowed_list.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


@login_required
@permission_required('catalog.can_mark_return', raise_exception=True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == "POST":

        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data['due_back']
            book_instance.save()

            return HttpResponseRedirect(reverse('my-borrowed'))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'due_back': proposed_renewal_date})

    context = {'form': form, 'book_instance': book_instance}
    return render(request, 'catalog/book_renew_librarian.html', context)


class AuthorCreate(CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'first_name': "Sir George"}


class AuthorUpdate(UpdateView):
    model = Author
    fields = "__all__"


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')


class BookCreate(CreateView):
    model = Book
    fields = "__all__"


class BookUpdate(UpdateView):
    model = Book
    fields = "__all__"


class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')
