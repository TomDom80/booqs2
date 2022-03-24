import os
from django.conf import settings
from django.forms.models import model_to_dict


def import_file_html(rec_path):
    folder_path = 'doctors/templates/doctors/'
    path = folder_path + rec_path
    file = open(os.path.join(settings.BASE_DIR, path), encoding='utf-8')
    ret_file = file.read()
    return ret_file


def get_key_list(receive_obj_arr):
    collected_keys = []
    for obj in receive_obj_arr:
        for key in obj.keys():
            if key not in collected_keys:
                collected_keys.append(key)

    return collected_keys


def create_table_service(rec_obj):
    row_objects = rec_obj.get('row_objects')
    received_keys_array = rec_obj.get('received_keys_array')
    colour = rec_obj.get('colour')
    title = rec_obj.get('title')
    edit_link = rec_obj.get('edit_link')
    delete_link = rec_obj.get('delete_link')

    """
            {{created_table | safe}}
            original_headers = get_key_list(receive_obj_arr)
    """

    if 'django.db.models.query.QuerySet' in str(type(row_objects)):
        some_list = []
        for obj in row_objects:
            dict_obj = model_to_dict(obj, fields=[field.name for field in obj._meta.fields])
            some_list.append(dict_obj)

        row_objects = some_list

    original_headers = get_key_list(row_objects)

    output_keys_array = []
    message = ''

    if received_keys_array:
        if '--' in received_keys_array:
            output_keys_array = original_headers
            for key in received_keys_array:
                if key in output_keys_array:
                    output_keys_array.remove(key)
        else:
            if not all([x in ''.join(original_headers) for x in received_keys_array]):
                new_header = []
                for header in received_keys_array:
                    if header not in original_headers:
                        message += f'there is no key: {header}'
                        message += f' [ {header} ] '
                        new_header.append(f'{header}_#?')
                    else:
                        new_header.append(header)
            output_keys_array = new_header
            message += f'<hr> Keys above doesn\'t exists'
    else:
        output_keys_array = original_headers

    message = ''
    table_in_string = ''
    table_in_string += '<div class="container">'
    if message:
        table_in_string += '<div class="row mt-3">' \
                   '<div class="col-12">' \
                   '<div class="alert alert-warning" role="alert">' \
                   '<h4 class="alert-heading">### message: ###</h4>' \
                   '<hr>' \
                   f'<p class="mb-0 text-break">{message}</p>' \
                   '</div>' \
                   '</div>' \
                   '</div>'

    table_in_string += '<div class="row mt-3">'
    table_in_string += '<div class="col-12">'

    # table_in_string += f'<table class="table table-bordered table-striped  table-primary align-middle text-center ">'

    table_in_string += f'<table class="table table-bordered  table-{colour} align-middle text-center ">'
    if title:
        table_in_string += '<thead> <tr>'
        table_in_string += f'<th style="width: "scope="col" colspan="100%" >{title}</th>'
        table_in_string += '</tr></thead><tbody>'

    table_in_string += '<thead> <tr>'
    for key in output_keys_array:
        table_in_string += f'<th style="width: " scope="col">{key}</th>'

    if edit_link:
        table_in_string += f'<th style="width: 5%" scope="col">Edit</th>'

    if delete_link:
        table_in_string += f'<th style="width: 5%" scope="col">Erase</th>'

    table_in_string += '</tr></thead><tbody>'

    for rec_obj in row_objects:
        table_in_string += '<tr class="text-center">'
        for key in output_keys_array:
            rec_obj_item = rec_obj.get(key, '')
            table_in_string += f'<td>{rec_obj_item}</td>'

        if edit_link:
            e_link = f'{edit_link + str(rec_obj.get("id"))}/'
            table_in_string += f'<td><a href="{e_link}"><i class="fa-solid fa-pen-to-square link-warning"></i></a></td>'
        if delete_link:
            del_link = f'{delete_link + str(rec_obj.get("id"))}/'
            table_in_string += f'<td><a href="{del_link}"><i class="fa-solid fa-trash-can link-danger"></i></a></td>'
        table_in_string += '</tr>'

    table_in_string += '</tbody>' \
                       '</table>' \
                       '</div>' \
                       '</div>' \
                       '</div>'

    return table_in_string

