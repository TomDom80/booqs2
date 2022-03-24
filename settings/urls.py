"""settings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter


from books import views as books_views
from books import viewsets as books_viewsets

from books.services import services

router = DefaultRouter()
router.register(r'books', books_viewsets.BookViewSet)
router.register(r'author', books_viewsets.AuthorViewSet)
router.register(r'lng', books_viewsets.PublicationLanguageViewSet)

urlpatterns = [

    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', books_views.index, name='index'),
    path('zadanie/', books_views.zadanie, name='zadanie'),

    path('import/', books_views.google_import, name='import_from_google'),
    path('import/<str:label>/', books_views.google_import, name='import_from_google'),
    path('books/', books_views.book_list, name='book_list'),
    path('authors/', books_views.authors_list, name='authors_list'),
    path('languages/', books_views.language_list, name='language_list'),

    path('book_delete/<int:pk>/', services.book_delete, name='book_delete'),
    path('book_delete/<str:title>/', services.book_delete, name='book_delete'),

    path('book_form/', books_views.book_form, name='book_form'),
    path('book_form/<int:pk>/', books_views.book_form, name='book_form'),

    path('autors_form/<str:model>/', books_views.auth_lang_form, name='auth_lang_form'),
    path('autors_form/<str:model>/<int:pk>/', books_views.auth_lang_form, name='auth_lang_form'),

    path('message/<str:message>/', books_views.message_service, name='message_service'),
    path('message/<str:message>/<str:colour>/', books_views.message_service, name='message_service'),


]
