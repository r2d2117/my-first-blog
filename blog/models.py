from django.db import models
from django.conf import settings
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_delete


# Create your models here.


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    postImg = models.ImageField(blank=True, upload_to='images/', default='images/no-image.jpg')

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    def __str__(self):
        return self.title


@receiver(post_delete, sender=Post)
def post_delete(sender, instance, **kwargs):
    instance.postImg.delete(False)



class Book(models.Model):
    title = models.CharField(max_length=100)
    isbn = models.IntegerField(unique=True)
    authors = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200, blank=True)
    publication_date = models.DateField()
    num_pages = models.IntegerField(blank=True, null=True)
    book_img = models.TextField(blank=True)
    description = models.TextField(blank=True)
    #about = models.ForeignKey('blog.About', on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title


class About(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, default='Thomas Woodfine-MacPherson', on_delete=models.CASCADE)
    aboutText = models.TextField()
    aboutImages = models.ImageField(blank=True, upload_to='aboutImages/', default='aboutImages/no-image.jpg')
    last_updated = models.DateTimeField(default=timezone.now)



    def publish(self):
        self.published_date = timezone.now()
        self.save()


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
