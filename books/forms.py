from django import forms
from .models import Book, Author, PublicationLanguage
from django.forms import ModelForm


class BookModelForm(ModelForm):
    class Meta:
        model = Book
        fields = "__all__"

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "authors": forms.SelectMultiple(attrs={"class": "form-select"}),
            "pub_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "isbn_nr": forms.TextInput(attrs={"class": "form-control"}),
            "pages_qty": forms.NumberInput(attrs={"class": "form-control"}),
            "cover_link": forms.TextInput(attrs={"class": "form-control"}),
            "pub_lang": forms.Select(attrs={"class": "form-select"}),
            "errors": forms.Select(attrs={"class": "is-invalid"}),
        }


class AuthorModelForm(ModelForm):
    class Meta:
        model = Author
        fields = "__all__"

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "surname": forms.TextInput(attrs={"class": "form-control"}),
        }


class LangModelForm(ModelForm):
    class Meta:
        model = PublicationLanguage
        fields = "__all__"

        widgets = {
            "lang": forms.TextInput(attrs={"class": "form-control"}),
        }
