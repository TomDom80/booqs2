from django.test import Client
from django.test import TestCase
from .forms import BookModelForm, LangModelForm, AuthorModelForm
from .services.import_service import set_my_book_title, set_my_book_authors,\
    set_my_book_published_date, count_validated

"""
Przykładowe testy...
"""


class TestServices(TestCase):
    def setUp(self):
        pass

    def test_set_my_book_title(self):
        sample_object = {
            'TMP': {},
            'is_valid': True
        }

        self.assertEqual(sample_object.get('is_valid'), True)
        # self.assertEqual(sample_object['title'], None)

        set_my_book_title(sample_object)

        self.assertEqual(sample_object.get('is_valid'), False)
        self.assertEqual(sample_object['title'], '[ ??? ]')

        sample_object['TMP']['title'] = 'some_new_title'
        set_my_book_title(sample_object)

        self.assertEqual(sample_object.get('is_valid'), False)
        self.assertEqual(sample_object['title'], 'some_new_title')

    def test_set_my_book_authors(self):
        sample_object = {
            'TMP': {'authors': ['John', 'Doe']},
            'is_valid': True
        }

        self.assertEqual(sample_object.get('is_valid'), True)
        set_my_book_authors(sample_object)
        self.assertEqual(sample_object['authors_string'], 'John, Doe')
        self.assertEqual(sample_object['authors_arr'], ['John', 'Doe'])

        sample_object = {
            'TMP': {},
            'is_valid': True
        }
        set_my_book_authors(sample_object)
        self.assertEqual(sample_object.get('is_valid'), False)
        self.assertEqual(sample_object['authors_string'], '')
        self.assertEqual(sample_object['authors_arr'], None)

    def test_set_my_book_published_date(self):
        sample_object = {
            'TMP': {'publishedDate': '2021-01-23'},
            'is_valid': True
        }

        self.assertEqual(sample_object.get('is_valid'), True)
        set_my_book_published_date(sample_object)
        self.assertEqual(sample_object.get('is_valid'), True)
        self.assertEqual(sample_object['pub_date'], '2021-01-23')

        sample_object = {
            'TMP': {'publishedDate': '2000-06'},
            'is_valid': True
        }
        set_my_book_published_date(sample_object)
        self.assertEqual(sample_object.get('is_valid'), False)
        self.assertEqual(sample_object['pub_date'], '2000-06 / [??]')

        sample_object = {
            'TMP': {'publishedDate': '2000'},
            'is_valid': True
        }
        set_my_book_published_date(sample_object)
        self.assertEqual(sample_object.get('is_valid'), False)
        self.assertEqual(sample_object['pub_date'], '2000 / [??]-[??]')
        sample_object = {
            'TMP': {'publishedDate': '20'},
            'is_valid': True
        }
        set_my_book_published_date(sample_object)
        self.assertEqual(sample_object.get('is_valid'), False)
        self.assertEqual(sample_object['pub_date'], '20 / [ ????? ]')

        sample_object = {
            'TMP': {},
            'is_valid': True
        }
        set_my_book_published_date(sample_object)
        self.assertEqual(sample_object.get('is_valid'), False)
        self.assertEqual(sample_object['pub_date'], '## ? ? ? ##')

        # self.assertContains()
        # self.asse

    def test_count_validated(self):

        p4_f2 = [
            {'is_valid': True},
            {'is_valid': True},
            {'is_valid': True},
            {'is_valid': True},
            {'is_valid': False},
            {'is_valid': False},
              ]

        self.assertEqual(count_validated(p4_f2).get('positive'), '4')
        self.assertEqual(count_validated(p4_f2).get('negative'), '2')
        self.assertEqual(count_validated(p4_f2).get('total_cnt'), '6')

        p2_f0 = [{'is_valid': True}, {'is_valid': True}]

        self.assertEqual(count_validated(p2_f0).get('positive'), '2')
        self.assertEqual(count_validated(p2_f0).get('negative'), '0')
        self.assertEqual(count_validated(p2_f0).get('total_cnt'), '2')

        p2_f0 = [{'is_valid': True}, {'is_valid': True}]

        self.assertEqual(count_validated(p2_f0).get('positive'), '2')
        self.assertEqual(count_validated(p2_f0).get('negative'), '0')
        self.assertEqual(count_validated(p2_f0).get('total_cnt'), '2')

        # self.asser


class TestPages(TestCase):
    def setUp(self):
        self.client = Client()

    def test_book_list_page(self):
        url = "/books/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "books/view_book_list/book_list.html")
        self.assertContains(response, "Create New Book")

    def test_google_import_page(self):
        url = "/import/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "books/view_import/google_import.html")
        self.assertContains(response, "Search in all Parameters")


class TestForms(TestCase):
    def test_empty_book_form(self):
        book_form = BookModelForm()

        self.assertInHTML(
            '<input type="text" name="title" class="form-control" required id="id_title">',
            str(book_form),
        )
        self.assertInHTML(
            '<select name="authors" class="form-select" required id="id_authors" multiple></select>',
            str(book_form),
        )
        self.assertInHTML(
            '<input type="date" name="pub_date" class="form-control" required id="id_pub_date">',
            str(book_form),
        )

    def test_empty_author_form(self):
        author_form = AuthorModelForm()

        self.assertInHTML(
            '<input type="text" name="name" class="form-control" maxlength="64" required id="id_name">',
            str(author_form),
        )
        self.assertInHTML(
            '<input type="text" name="surname" class="form-control" maxlength="64" required id="id_surname">',
            str(author_form),
        )

    def test_empty_language_form(self):
        lang_form = LangModelForm()

        self.assertInHTML(
            '<input type="text" name="lang" class="form-control" maxlength="15" id="id_lang">',
            str(lang_form),
        )



