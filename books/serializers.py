from rest_framework import serializers
from .models import Book, Author, PublicationLanguage


class PublicationLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicationLanguage
        fields = "__all__"


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"
