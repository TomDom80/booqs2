from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import Book
from django.shortcuts import redirect


@csrf_exempt
def book_delete(request, pk=-1, title="none"):
    if Book.objects.filter(id=pk).exists():
        try:
            Book.objects.filter(id=pk).delete()
            return redirect("book_list")
        except Exception as e:
            return redirect("message_service", message=str(e))

    if Book.objects.filter(title=title).exists():
        try:
            Book.objects.filter(title=title).delete()
            return redirect("book_list")
        except Exception as e:
            return redirect("message_service", message=str(e))

    return HttpResponse("Error: title = %s , id = %d." % (title, pk))
