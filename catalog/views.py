import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Book
from .forms import RenewBookModelForm
from .models import Book, Author, BookInstance, Genre
# Create your views here.

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_genres = Genre.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()
    num_visits = request.session.get('num_visits', 0)
    num_visits += 1
    request.session['num_visits'] = num_visits
    
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_visits': num_visits
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'book_list.html'
    paginate_by = 2
    
    def get_queryset(self):
        return Book.objects.all()


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'book_detail.html'


class AuthorListView(generic.ListView):
    model = Author
    template_name = 'author_list.html'
    paginate_by = 3

class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'author_detail.html'

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    model = BookInstance
    template_name = 'bookinstance_list_borrowed_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )
        
class AllBorrowedBooks(PermissionRequiredMixin, generic.ListView):
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name = 'all_borrowed_books.html'
    paginate_by = 2
    def get_queryset(self):
        return (
            BookInstance.objects.filter(status__exact='o').exclude(borrower=None)
        )


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)      
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)
    
    if request.method == 'POST':
        form = RenewBookModelForm(request.POST)
        
        if form.is_valid():
            book_instance.due_back = form.cleaned_data['due_back']
            
            book_instance.save()
            
            return HttpResponseRedirect(reverse('catalog:all-borrowed'))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=4)
        form = RenewBookModelForm(initial={'due_back': proposed_renewal_date})
        
    context = {
        'form': form,
        'book_instance': book_instance
    }
        
    return render(request, 'book_renew_librarian.html', context)
            
            
class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    template_name = 'author_form.html'
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    # initial = {'date_of_death': '11/11/2023'}
    permission_required = 'catalog.add_author'

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    template_name = 'author_form.html'
    # Not recommended (potential security issue if more fields added)
    fields = '__all__'
    permission_required = 'catalog.change_author'

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('catalog:authors')
    permission_required = 'catalog.delete_author'
    template_name = 'author_confirm_delete.html'
    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse("catalog:author-delete", kwargs={"pk": self.object.pk})
            )