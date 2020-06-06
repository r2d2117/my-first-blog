from blog.services import get_books_data
from django.shortcuts import render


# Create your views here.


def search(request):
    query = request.GET.get('q')
    books = get_books_data(query)
    return render(request, 'book_list.html', {'books': books})
