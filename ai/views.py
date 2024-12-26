from rest_framework.viewsets import (
    ModelViewSet
)

from rest_framework.views import (
    APIView,
    Response
)

from .models import (
    AIQuestionStore as AIQuestionStoreModel
)

from .serializers import (
    AIQuestion as AIQuestionSerializer,
    AITraining as AITrainingSerializer,
)

from drf_spectacular.utils import (
    extend_schema
)

from copy import deepcopy

global st_response_json
st_response_json = {
    'status': 'error',
    'errors': [
        
    ],
    'response_message': ''
}

class AITraining(APIView):
    serializer_class = AITrainingSerializer

    @extend_schema(
        request=AITrainingSerializer
    )
    def post(self, request, *args, **kwargs):
        response_json = deepcopy(st_response_json)

        try:
            data = request.data
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            train_response = serializer.train(
                serializer.validated_data
            )
            response_json['response_message'] = train_response
            response_json['status'] = 'success'

        except (Exception, ) as e:
            if hasattr(e, 'detail'):
                response_json['errors'] = e.detail
            else:
                response_json['errors'].append(str(e))
        
        finally:
            return Response(response_json)

class AIQuestion(ModelViewSet):
    queryset = AIQuestionStoreModel.objects.using('ai').all()
    serializer_class = AIQuestionSerializer

    @extend_schema(
        request=AIQuestionSerializer
    )
    def send_question(self, request, *args, **kwargs):
        response_json = deepcopy(st_response_json)

        try:
            data = request.data
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            response_json['response_message'] = 'Answer question sent to your email'
            response_json['status'] = 'success'

        except (Exception, ) as e:
            if hasattr(e, 'detail'):
                response_json['errors'] = e.detail
            else:
                response_json['errors'].append(str(e))
        
        finally:
            return Response(response_json)