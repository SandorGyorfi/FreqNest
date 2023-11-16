import logging

from django.http import HttpResponse, HttpResponseServerError

def custom_error_view(request):
    try:
        result = 1 / 0  
        return HttpResponse("Result: " + str(result))
    except Exception as e:
        logging.error("An error occurred: %s" % str(e))
        return HttpResponseServerError("An error occurred")

