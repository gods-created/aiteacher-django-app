from rest_framework.serializers import (
    Serializer,
    ModelSerializer,
    CharField,
    EmailField,
    JSONField,
    ValidationError
)

from minions import (
    start_training,
)

from .models import (
    AIQuestionStore as AIQuestionStoreModel
)

from .tasks import (
    send_answer,
)

class AITraining(Serializer):
    data = JSONField(
        default = [
            {
                'question': 'How many two plus two?', 
                'answer': '4'
            },
            {
                'question': 'Who invented radio?', 
                'answer': 'Heinrich Rudolf Hertz'
            }
        ]
    )

    def validate(self, attr):
        for item, value in attr.items():
            default_value = self.fields[item].default
            if value == default_value:
                raise ValidationError(
                    'You can\'t send default value from each field'
                )

        return attr

    def validate_data(self, value):
        if not isinstance(value, list):
            raise ValidationError(
                'The \'data\' field have to be list'
            )
        
        if len(value) <= 500:
            raise ValidationError(
                'The \'data\' field have to have more than 500 values'
            )
        
        return value
    
    def train(self, validated_data):
        data = validated_data.get('data', [])
        start_training_response = start_training(data)
        return start_training_response

class AIQuestion(ModelSerializer):
    class Meta:
        model = AIQuestionStoreModel
        fields = ['email', 'question']

    email = EmailField(
        required=True,
        max_length=50,
        error_messages={
            'required': 'The \'email\' field is required',
            'max_length': 'The \'email\' field have to have max 50 characters'
        }
    )

    question = CharField(
        required=True,
        min_length=1,
        max_length=1000,
        error_messages={
            'required': 'The \'question\' field is required',
            'min_length': 'The \'question\' field have to have min 1 character',
            'max_length': 'The \'question\' field have to have max 1000 characters'
        }
    )

    def create(self, validated_data):
        send_answer_task = send_answer.apply_async(
            (None),
            validated_data,
            queue='high_priority'
        )

        return AIQuestionStoreModel.objects.using('ai').create(
            **validated_data
        )