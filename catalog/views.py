from django.shortcuts import render

# Create your views here.
from catalog.models import Book, Author, BookInstance, Genre
from django.contrib.auth.decorators import login_required
@login_required

def index(request):
	"""View function for home page of site."""
	my_container = 'w'

	# Generate counts of some of the main objects
	num_books = Book.objects.filter(genre__name__icontains = my_container).count()
	num_instances = BookInstance.objects.all().count()

	# Available books (status = 'a')
	num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    
    # The 'all()' is implied by default.    
	num_authors = Author.objects.count()
	
	# Available genres (icontains = my_contain)
	num_genres = Genre.objects.filter(name__icontains = my_container).count()
    
	num_authors = Author.objects.count()  # The 'all()' is implied by default.
    
	# Number of visits to this view, as counted in the session variable.
	num_visits = request.session.get('num_visits', 0)
	request.session['num_visits'] = num_visits + 1
	
	
	context = {
		'num_books': num_books,
		'num_instances': num_instances,
		'num_instances_available': num_instances_available,
		'num_authors': num_authors,
		'my_container' : my_container,
		'num_genres': num_genres,
		'num_visits': num_visits,
		}
		
	# Render the HTML template index.html with the data in the context variable
	return render(request, 'index.html', context=context)


	
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

class BookListView(LoginRequiredMixin, generic.ListView):
    
	model = Book
	paginate_by = 2
	#context_object_name = 'my_book_list'   
	#context_object_name = 'book_list'   # your own name for the list as a template variable
	#queryset = Book.objects.filter(title__icontains='1')[:2] # Get 5 books containing the title war
	#template_name = 'catalog/book_list.html'  # Specify your own template name/location
	
	
class BookDetailView(generic.DetailView):
    """Generic class-based detail view for a book."""
    model = Book
	
class AuthorListView(LoginRequiredMixin, generic.ListView):
    
	model = Author
	'''paginate_by = 2'''

class AuthorDetailView(generic.DetailView):
    
	model = Author
	'''paginate_by = 2'''	

from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


from django.contrib.auth.mixins import  PermissionRequiredMixin

class LoanedBooksByStaffListView(PermissionRequiredMixin, generic.ListView):
	"""Generic class-based view listing books on loan to staff user."""
	permission_required = 'catalog.can_mark_returned'
	model = BookInstance
	template_name = 'catalog/bookinstance_list_borrowed_staff.html'
	paginate_by = 10

	def get_queryset(self):
		return BookInstance.objects.filter(status__exact='o').order_by('due_back')

import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from catalog.forms import RenewBookForm

def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
			# return HttpResponseRedirect(reverse('all-borrowed') )
            return HttpResponseRedirect(reverse('staff-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)
	
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from catalog.models import Author

class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '05/01/2018'}

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
	
