from django.http import HttpResponse

def custom_error_view(request):
    return HttpResponse("An error occurred", status=500)
