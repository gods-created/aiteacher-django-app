from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    ValidationError
)

from .models import (
    Key as KeyModel
)

from minions import (
    generate_api_key
)

from drf_spectacular.utils import extend_schema_field

class Key(ModelSerializer):
    class Meta:
        model = KeyModel
        fields = '__all__'
        read_only_fields = [
            'api_key'
        ]

    api_key = SerializerMethodField()

    @extend_schema_field(str)
    def get_api_key(self, value):
        value = generate_api_key()
        value_length = len(value)
        if not 10 <= value_length <= 30:
            raise ValidationError(
                'The \'api_key\' have to have from 10 to 30 characters. Need to fix \'generate_api_key\' function'
            )
        
        if KeyModel.objects.using('keys').filter(api_key=value).exists():
            return self.get_api_key(value)

        return value
        
    def create(self, *args, **kwargs):
        api_key = self.get_api_key(
            self.initial_data.get('api_key')
        )
        return KeyModel.objects.using('keys').create(
            api_key=api_key
        )

