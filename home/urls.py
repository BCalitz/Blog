from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('admin/', admin.site.urls),
    path('blog/<int:blog_id>', views.blog, name='blog'),
    path('author/', views.authors, name='authors'),
    path('author/<int:author_id>', views.author, name='author'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('signup', views.signup, name='signup'),
    path('post', views.post, name='post'),
]
