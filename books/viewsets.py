from rest_framework import viewsets
from .models import Book, Author, PublicationLanguage
from .serializers import AuthorSerializer, BookSerializer, PublicationLanguageSerializer

from django_filters import rest_framework as filters
from django_filters import FilterSet


class BookFilter(FilterSet):

    class Meta:
        model = Book
        fields = {
            'title': ['exact', 'icontains', 'contains'],
            'authors': ['exact', 'icontains', 'contains'],

            'id': ['exact', 'range', 'gt', 'lt'],
            'pages_qty': ['exact', 'range', 'gt', 'lt'],
            'isbn_nr': ['exact', 'range', 'gt', 'lt'],

            'pub_date': ['exact', 'range', 'year__exact',  'year__gt', 'year__lt', 'gt', 'lt'],
            'pub_lang': ['exact'],
        }


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = BookFilter


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class PublicationLanguageViewSet(viewsets.ModelViewSet):
    queryset = PublicationLanguage.objects.all()
    serializer_class = PublicationLanguageSerializer
