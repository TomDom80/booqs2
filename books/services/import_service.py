import requests
import json
from ..models import Book, Author, PublicationLanguage
from django.conf import settings
from django.shortcuts import redirect


def set_start_end_index(send_obj):
    search_plus = int(send_obj.get("search_plus", 0))
    search_minus = int(send_obj.get("search_minus", 0))
    start_index = int(send_obj.get("start_index", 0))
    total_items = int(send_obj.get("total_items", 0))

    start_index = start_index + search_plus - search_minus

    if start_index < 0:
        start_index = 0
    elif start_index > 0 and start_index >= total_items:
        start_index = total_items
        pass

    send_obj["end_index"] = start_index + 40
    send_obj['start_index'] = int(start_index)


def set_api_query(send_obj):
    api_query = ""
    if send_obj['b_query'] != "":
        api_query += send_obj['b_query']

    if send_obj['b_title'] != "":
        if len(api_query) > 0:
            api_query += "+"
        api_query += "intitle:" + send_obj['b_title']

    if send_obj['b_author'] != "":
        if len(api_query) > 0:
            api_query += "+"
        api_query += "inauthor:" + send_obj['b_author']

    send_obj['api_query'] = api_query

    return api_query


def get_total_items(response):
    total_items = 0
    if response:
        total_items = response.json().get("totalItems")
        total_items = int(total_items)

    return total_items


def request_to_api_google(send_obj):
    api_query = send_obj['api_query']
    err_message = ""
    except_message = ""
    response = None
    resp_items_go_api = None
    if api_query:
        try:
            google_apikey = settings.GOOGLE_API_KEY
            params = {
                "q": api_query,
                "startIndex": send_obj['start_index'],
                "maxResults": 40,
                "key": google_apikey,
            }
            response = requests.get(
                "https://www.googleapis.com/books/v1/volumes", params=params
            )

            if "error" in response.json():
                err_message = response.json().get("error")

            response.raise_for_status()  # Additional code will only run if the request is successful
            resp_items_go_api = response.json().get("items")

        except requests.exceptions.HTTPError as errh:
            except_message += " Http Error:" + str(errh)
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            except_message += " Error Connecting:" + str(errc)
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            except_message += " Timeout Error:" + str(errt)
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            except_message += " OOps: Something Else:" + str(err)
            print("OOps: Something Else", err)

    send_obj['total_items'] = get_total_items(response)

    send_obj['message']['yellow'] += str(except_message)
    send_obj['message']['red'] += str(err_message)

    return resp_items_go_api


def set_my_book_title(received_object):
    title = received_object['TMP'].get("title")

    if title:
        received_object['title'] = title
    else:
        received_object['is_valid'] = False
        received_object['title'] = '[ ??? ]'


def set_my_book_authors(received_object):
    authors_arr = received_object['TMP'].get("authors")

    authors_string = ''
    if authors_arr:
        authors_string = ', '.join(authors_arr)
    else:
        received_object['is_valid'] = False
        received_object['authors_string'] = '???'

    received_object['authors_arr'] = authors_arr
    received_object['authors_string'] = authors_string


def set_my_book_published_date(received_object):
    publication_date = received_object['TMP'].get("publishedDate")
    str_pub_date = str(publication_date)
    lng_pub_date = len(str_pub_date)
    if publication_date:
        if lng_pub_date == 10:
            received_object['pub_date'] = publication_date
        elif lng_pub_date == 4:
            received_object['is_valid'] = False
            received_object['pub_date'] = f'{str_pub_date} / [??]-[??]'
        elif lng_pub_date == 7:
            received_object['is_valid'] = False
            received_object['pub_date'] = f'{str_pub_date} / [??]'
        else:
            received_object['is_valid'] = False
            received_object['pub_date'] = f'{str_pub_date} / [ ????? ]'
    else:
        received_object['is_valid'] = False
        received_object['pub_date'] = '## ? ? ? ##'


def set_my_book_language(received_object):
    language = received_object['TMP'].get("language")

    if language:
        received_object['pub_lang'] = language
    else:
        received_object['is_valid'] = False
        received_object['pub_lang'] = '[ ? ]'


def set_my_book_pages_qty(received_object):
    pages_qty = received_object['TMP'].get("pageCount")

    if pages_qty:
        if int(pages_qty) < 0:
            received_object['is_valid'] = False
            received_object['pages_qty'] = f'{pages_qty} / [ ? ]'
        else:
            received_object['pages_qty'] = pages_qty
    else:
        received_object['is_valid'] = False
        received_object['pages_qty'] = '[ ? ]'


def set_my_book_isbn_nr(received_object):
    isbn_nr_arr = received_object['TMP'].get("industryIdentifiers")
    isbn = ''

    if isbn_nr_arr and len(isbn_nr_arr) >= 2:
        isbn = isbn_nr_arr[1].get("identifier")
        if isbn:
            if isbn.isdecimal():
                if len(isbn) == 10 or len(isbn) == 13:
                    received_object['isbn_nr'] = isbn
                else:
                    received_object['is_valid'] = False
                    received_object['isbn_nr'] = f'{isbn} [ len({len(isbn)}) ]'
            else:
                received_object['is_valid'] = False
                received_object['isbn_nr'] = f'{isbn} !!!_decimal_???'
        else:
            received_object['is_valid'] = False
            received_object['isbn_nr'] = f'{isbn}[ ?????????? ]'
    else:
        received_object['is_valid'] = False
        received_object['isbn_nr'] = '[ ?????????? ]'


def set_my_book_preview_link(received_object):
    preview_link = received_object['TMP'].get("previewLink")

    if preview_link:
        received_object['preview_link'] = preview_link
    else:
        received_object['is_valid'] = False
        received_object['preview_link'] = '[ ??? ]'


def set_my_book_cover_link(received_object):
    image_links = received_object['TMP'].get("imageLinks")

    if image_links:
        # small_thumbnail = image_links.get("smallThumbnail")
        small_thumbnail = image_links.get("thumbnail")
        if small_thumbnail:
            received_object['cover_link'] = small_thumbnail
        else:
            received_object['is_valid'] = False
    else:
        received_object['is_valid'] = False


def set_my_book_imported_already(received_object):
    title = received_object.get("title")

    if title and Book.objects.filter(title=title).exists():
        received_object['imported_already'] = True


def set_my_book_cleaned(received_object):
    del received_object['TMP']


def set_my_book_labels(received_object):
    isbn_nr = received_object.get("isbn_nr")

    if isbn_nr:
        received_object['labels'] = f"label_{isbn_nr}"


def check_validation_of_object_google(received_object):
    my_book = {"is_valid": True, }

    volume_info = received_object.get("volumeInfo")
    if volume_info:
        my_book['TMP'] = volume_info

        set_my_book_title(my_book)
        set_my_book_authors(my_book)
        set_my_book_published_date(my_book)
        set_my_book_language(my_book)
        set_my_book_pages_qty(my_book)
        set_my_book_isbn_nr(my_book)
        # set_my_book_preview_link(my_book)
        set_my_book_cover_link(my_book)
        set_my_book_imported_already(my_book)
        set_my_book_labels(my_book)

        set_my_book_cleaned(my_book)

    else:
        my_book['is_valid'] = False

    return my_book


def count_validated(google_objects):
    positive = 0
    negative = 0
    if google_objects:
        for g_book in google_objects:
            is_valid = g_book['is_valid']
            if is_valid:
                positive += 1
            else:
                negative += 1

    return {'positive': str(positive), 'negative': str(negative), 'total_cnt': str(positive + negative)}


def get_data_from_google_objects(google_objects):
    google_book_list = []
    if google_objects:
        for g_book in google_objects:
            my_book = check_validation_of_object_google(g_book)

            my_book_json = json.dumps(my_book)
            my_book["js_book"] = my_book_json
            google_book_list.append(my_book)

    return google_book_list


def save_google_book_obj(book_obj):
    authors_arr = book_obj.get("authors_arr")
    auth_instance_arr = []
    name = ''
    surname = ''
    for auth in authors_arr:
        sep_auth = auth.split(' ')
        if len(sep_auth) >= 2:
            name = ' '.join(sep_auth[0:-1])
            surname = sep_auth[-1]
        elif len(sep_auth) >= 1:
            name = auth[0]

        if Author.objects.filter(name=name, surname=surname).exists():
            try:
                auth_instance = Author.objects.get(name=name, surname=surname)
                auth_instance_arr.append(auth_instance)
            except Exception as e:
                return redirect("message_service", message=str(e))

        else:
            try:
                Author(name=name, surname=surname).save()
                auth_instance = Author.objects.get(name=name, surname=surname)
                auth_instance_arr.append(auth_instance)
            except Exception as e:
                return redirect("message_service", message=str(e))

    lang = book_obj.get("pub_lang")
    if PublicationLanguage.objects.filter(lang=lang).exists():
        try:
            lang_instance = PublicationLanguage.objects.get(lang=lang)
        except Exception as e:
            return redirect("message_service", message=str(e))
    else:
        try:
            PublicationLanguage(lang=lang).save()
            lang_instance = PublicationLanguage.objects.get(lang=lang)
        except Exception as e:
            return redirect("message_service", message=str(e))

    title = book_obj.get("title")
    isbn_nr = book_obj.get("isbn_nr")
    if not Book.objects.filter(title=title, isbn_nr=isbn_nr).exists():

        book_instance = Book(
            title=title,
            # authors,
            pub_date=book_obj.get("pub_date"),
            isbn_nr=isbn_nr,
            pages_qty=book_obj.get("pages_qty"),
            cover_link=book_obj.get("cover_link"),
            pub_lang=lang_instance,
        )
        try:
            book_instance.save()

            for auth in auth_instance_arr:
                book_instance.authors.add(auth)

            book_instance.save()

            return "Book was saves successfully !!!"
        except Exception as e:
            return str(e)

    else:
        return "### Error: ###   ISBN / Title already exists..."


def save_if_need(query_string, send_obj):
    save_obj = query_string.get("save_book_obj")

    if save_obj:
        book_obj = json.loads(save_obj)
        effect = save_google_book_obj(book_obj)

        if effect != "Book was saves successfully !!!":
            send_obj['message']['red'] += str(effect)
        else:
            send_obj['message']['green'] += effect
            pass

    # return effect


def send_object_create(query_string):
    send_obj = {}
    send_obj_str = json.dumps(send_obj)
    send_obj_json = query_string.get("send_obj_json", send_obj_str)
    send_obj = json.loads(send_obj_json)

    send_obj['b_query'] = query_string.get('query', send_obj.get('b_query', ''))
    send_obj['b_title'] = query_string.get('title', send_obj.get('b_title', ''))
    send_obj['b_author'] = query_string.get('author', send_obj.get('b_author', ''))
    send_obj['start_index'] = int(query_string.get('start_index', send_obj.get('start_index', 0)))

    send_obj['search_plus'] = int(query_string.get('search_plus', 0))
    send_obj['search_minus'] = int(query_string.get('search_minus', 0))

    send_obj['show_all'] = type(query_string.get("to_show_all")) == str

    send_obj['message'] = {
        "green": '',
        "yellow": '',
        "red": '',
    }
    send_obj['message']['green'] = ''
    send_obj['message']['yellow'] = ''
    send_obj['message']['red'] = ''

    return send_obj


def service_for_google_import(query_string):
    send_obj = send_object_create(query_string)
    save_if_need(query_string, send_obj)

    set_start_end_index(send_obj)
    set_api_query(send_obj)

    ob_google_resp = request_to_api_google(send_obj)

    google_book_list = get_data_from_google_objects(ob_google_resp)
    count = count_validated(google_book_list)

    # ################################################ #
    send_obj_json = json.dumps(send_obj)
    # ################################################ #
    send_obj['google_book_list'] = google_book_list
    send_obj['positive'] = count['positive']
    send_obj['negative'] = count['negative']

    # send_obj['message']['green'] = ob_google_resp
    return {'send_obj': send_obj, 'send_obj_json': send_obj_json, }
