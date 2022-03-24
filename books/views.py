from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from .models import Book, Author, PublicationLanguage
from .forms import BookModelForm, AuthorModelForm, LangModelForm
from .services.tables_service import create_table_service
from .services.import_service import service_for_google_import


@csrf_exempt
def book_form(request, pk=0):
    if request.method == "POST":
        if pk > 0:
            try:
                book_instance = Book.objects.get(id=pk)
                form = BookModelForm(request.POST, instance=book_instance)
            except Exception as e:
                return redirect("message_service", message=str(e))
        else:
            form = BookModelForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect("book_list")
            except Exception as e:
                return redirect("message_service", message=str(e))
    elif pk > 0:
        try:
            book_instance = Book.objects.get(id=pk)
            form = BookModelForm(instance=book_instance)
        except Exception as e:
            return redirect("message_service", message=str(e))
    else:
        form = BookModelForm()

    return render(request, "books/forms/book_form.html", {"form": form, "id": pk})


@csrf_exempt
def auth_lang_form(request, model=None, pk=0):
    if model == "author":
        if request.method == "POST":
            if pk > 0:
                try:
                    author_instance = Author.objects.get(id=pk)
                    form = AuthorModelForm(request.POST, instance=author_instance)
                except Exception as e:
                    return redirect("message_service", message=str(e))
            else:
                form = AuthorModelForm(request.POST)
            if form.is_valid():
                try:
                    form.save()
                    return redirect("authors_list")
                except Exception as e:
                    return redirect("message_service", message=str(e))
        elif pk > 0:
            try:
                author_instance = Author.objects.get(id=pk)
                form = AuthorModelForm(instance=author_instance)
            except Exception as e:
                return redirect("message_service", message=str(e))
        else:
            form = AuthorModelForm()

    elif model == "language":
        if request.method == "POST":
            if pk > 0:
                try:
                    language_instance = PublicationLanguage.objects.get(id=pk)
                    form = LangModelForm(request.POST, instance=language_instance)
                except Exception as e:
                    return redirect("message_service", message=str(e))
            else:
                form = LangModelForm(request.POST)
            if form.is_valid():
                try:
                    form.save()
                    return redirect("language_list")
                except Exception as e:
                    return redirect("message_service", message=str(e))
        elif pk > 0:
            try:
                language_instance = PublicationLanguage.objects.get(id=pk)
                form = LangModelForm(instance=language_instance)
            except Exception as e:
                return redirect("message_service", message=str(e))
        else:
            form = LangModelForm()

    elif model == "author_delete" and pk > 0:
        if Author.objects.filter(id=pk).exists():
            try:
                Author.objects.filter(id=pk).delete()
                return redirect("authors_list")
            except Exception as e:
                return redirect("message_service", message=str(e))

    elif model == "language_delete" and pk > 0:
        if PublicationLanguage.objects.filter(id=pk).exists():
            try:
                PublicationLanguage.objects.filter(id=pk).delete()
                return redirect("language_list")
            except Exception as e:
                return redirect("message_service", message=str(e))

    else:
        return redirect("book_list")

    return render(
        request, "books/forms/auth_lang_form.html", {"form": form, "id": pk, "model": model}
    )


@csrf_exempt
def book_list(request):
    query_string = request.GET
    # b_query = query_string.get("query", "")
    b_title = query_string.get("title", "")
    b_author = query_string.get("author", "")
    b_lang = query_string.get("lang", "")
    bs_date = query_string.get("start_date", "")
    be_date = query_string.get("end_date", "")

    send_obj = {'message': {}}

    if bs_date:
        ss_date = bs_date
    else:
        ss_date = '0001-01-01'

    if be_date:
        se_date = be_date
    else:
        se_date = '9999-01-01'

    if (
            b_title == ""
            and b_author == ""
            and bs_date == ""
            and be_date == ""
            and b_lang == ""
    ):
        book_list_objects = Book.objects.all()
    else:
        book_list_objects = Book.objects.filter(
            Q(title__icontains=b_title),
            Q(authors__name__icontains=b_author) | Q(authors__surname__icontains=b_author),
            Q(pub_lang__lang__icontains=b_lang),
            Q(pub_date__gt=ss_date) & Q(pub_date__lt=se_date),
        ).distinct()

    # available_authors = Author.objects.all()
    # available_lang = PublicationLanguage.objects.all()
    context = {
        "send_obj": send_obj,
        "available_authors": Author.objects.all(),
        "available_lang": PublicationLanguage.objects.all(),
        "book_list_objects": book_list_objects,
        "b_title": b_title,
        "b_author": b_author,
        "b_lang": b_lang,
        "bs_date": bs_date,
        "be_date": be_date,
        "title": "Book List",
    }

    return render(request, "books/view_book_list/book_list.html", context)


@csrf_exempt
def google_import(request, label=''):
    query_string = request.GET

    serv_imp = service_for_google_import(query_string)

    context = {
        "send_obj_json": serv_imp['send_obj_json'],
        "send_obj": serv_imp['send_obj'],

        "last_import": query_string.get("last_import"),
        "title": "Google Import",
    }

    return render(request, "books/view_import/google_import.html", context)


@csrf_exempt
def authors_list(request):
    list_of_authors = Author.objects.all()
    created_table = create_table_service(
        {
            "row_objects": list_of_authors,
            "received_keys_array": [],
            "colour": '',
            "title": 'List of Authors',
            "edit_link": '/autors_form/author/',
            "delete_link": '/autors_form/author_delete/',
        }
    )

    send_obj = {'message': {}}
    context = {
        "send_obj": send_obj,
        "created_table": created_table,
        "title": "Authors",
    }
    return render(request, "books/components/blank_for_creation.html", context)


@csrf_exempt
def language_list(request):
    list_of_lng = PublicationLanguage.objects.all()
    created_table = create_table_service(
        {
            "row_objects": list_of_lng,
            "received_keys_array": [],
            "colour": '',
            "title": 'Languages List',
            "edit_link": '/autors_form/language/',
            "delete_link": '/autors_form/language_delete/',
        }
    )

    send_obj = {'message': {}}
    context = {
        "send_obj": send_obj,
        "created_table": created_table,
        "title": "Languages",
    }
    return render(request, "books/components/blank_for_creation.html", context)


@csrf_exempt
def message_service(request, message='', colour=''):
    send_obj = {'message': {}}

    if colour == 'green':
        send_obj['message']['green'] = message
    elif colour == 'yellow':
        send_obj['message']['yellow'] = message
    else:
        send_obj['message']['red'] = message

    context = {
        "send_obj": send_obj,
        "title": "Message",
    }
    return render(request, "books/components/message_service.html", context)


@csrf_exempt
def index(request):
    q_link = [
        "Search by TITLE",
        "?title__icontains=hobbit",
        "?title__icontains=red",
        "?title__icontains=ACE",
        "Search by DATE",
        "?pub_date__range=2008-01-01,2012-01-01",
        "?pub_date__year=2012",
        "?pub_date__year=2021",
        "?pub_date__gt=2017-01-01",
        "?pub_date__lt=2017-01-01",
        "Search by PAGES QTY",
        "?pages_qty=300",
        "?pages_qty__range=50,200",
        "?pages_qty__range=200,300",
        "?pages_qty__gt=400",
        "?pages_qty__gt=200",
        "?pages_qty__lt=200",
        "?pages_qty__lt=50",
        "Search by ISBN",
        "?isbn_nr=0226036332",
        "?isbn_nr__gt=0547951973",
        "?isbn_nr__gt=1000000000",
        "?isbn_nr__lt=1000000000",
        "?isbn_nr__range=1000000000,2000000000",
        "Search by MIX",
        "?title__contains=hobbit&pub_date__year=2009",
        "?title__contains=hobbit&pub_date__year=2012",
        "?title__contains=hobbit&pub_date__year=2013",
        "?title__contains=hobbit&pub_date__lt=2012-01-01",
    ]

    context = {
        "q_link": q_link,
        "title": "INDEX",
    }
    return render(request, "books/index.html", context)


@csrf_exempt
def zadanie(request):
    context = {
        "title": "Zadanie",
    }
    return render(request, "books/zadanie.html", context)
