from django.urls import resolve
from django.http import HttpResponse
from apikey.models import (
    Key as KeyModel
)

class Error403:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            path = request.path
            match = resolve(path)
            if match.app_name != 'ai':
                return self.get_response(request)
            
            api_key = request.headers.get('Authorization', '')
            if_key_exists = KeyModel.objects.using('keys').filter(api_key=api_key).exists()
            if not if_key_exists:
                return HttpResponse(
                    'Error 403: forbidden',
                    status=403
                )

            return self.get_response(request)
        
        except (Exception, ) as e:
            return HttpResponse(
                f'Error 500: {str(e)}',
                status=500
            )