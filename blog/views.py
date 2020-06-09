from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from blog.services import get_books_data
from .forms import PostForm, CommentForm, AboutForm, BookForm
from .models import Post, Comment, About, Book
from django.template.defaulttags import register
from django.http import HttpResponse, HttpResponseRedirect
import datetime
import ast

from pprint import pprint


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def about(request):
    about_text = get_object_or_404(About)
    return render(request, 'blog/about.html', {'about': about_text})


@login_required
def about_edit(request):
    about = get_object_or_404(About)
    if request.method == "POST":
        form = AboutForm(request.POST, request.FILES, instance=about)
        if form.is_valid():
            about.delete()
            about = form.save(commit=False)
            about.save()
            return redirect('about')
    else:
        form = AboutForm(instance=about)
    return render(request, 'blog/about_edit.html', {'form': form})


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user

            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user

            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)


# def books(request, isbn):
#     books = get_object_or_404(Book, isbn=isbn)
#     return render(request, 'blog/bookshelf.html', {'books': books})

def bookshelf(request):
    if request.method == 'POST':
        return add_book_to_shelf(request)
    else:
        return search(request)

@login_required()
def add_book_to_shelf(request):
    r = request.POST.dict()

    tt = ast.literal_eval(r['isbn'])

    book = Book()
    both_isbn = {}
    for item in tt:
        pair = {item['type']: item['identifier']}
        both_isbn.update(pair)
    # print(both_isbn)

    if 'ISBN_13' in both_isbn:
        book.isbn = both_isbn['ISBN_13']
    else:
        book.isbn = both_isbn['ISBN_10']

    book.title = r['title']
    book.num_pages = r['pagecount']
    book.description = r['textSnippet']
    book.publication_date = r['publication_date']
    book.book_img = r['img']
    book.authors = r['authors']
    book.save()
    return redirect('bookshelf')

@login_required()
def delete_book(request, isbn):
    book = Book.objects.get(isbn=int(isbn))
    book.delete()
    return redirect('bookshelf')


def search(request):
    query = request.GET.get('q', '')
    my_books = Book.objects.all()
    if query:
        books = get_books_data(query)
        results = books['items']
        pprint(results[1], width=80)
    else:
        results = []
        # print('here')

    return render(request, 'bookshelf/book_list.html', {'results': results, 'books': my_books})
