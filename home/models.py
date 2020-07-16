from django.db import models


class Author(models.Model):

    author_fname = models.CharField(max_length=64)
    author_sname = models.CharField(max_length=64)
    author_email = models.EmailField(max_length=254)
    author_pass = models.CharField(max_length=15)
    def __str__(self):
        return f"{self.author_fname} {self.author_sname}"


class Blog(models.Model):

    blog_title = models.CharField(max_length=100)
    blog_context = models.TextField()
    blog_author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    blog_date = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.blog_title}"

