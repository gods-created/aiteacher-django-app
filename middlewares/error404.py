from django.urls import resolve, Resolver404
from django.http import HttpResponse

class Error404:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            path = request.path
            resolve(path)

        except (Resolver404, ):
            return HttpResponse(
                'Error 404: page not found',
                status=404
            )

        return self.get_response(request)