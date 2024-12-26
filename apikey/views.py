from rest_framework.viewsets import (
    ModelViewSet
)

from .models import (
    Key as KeyModel
)

from .serializers import (
    Key as KeySerializer
)

class Key(ModelViewSet):
    queryset = KeyModel.objects.using('keys').all()
    serializer_class = KeySerializer
    http_method_names = ['post', 'delete']