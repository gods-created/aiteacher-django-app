from django.db.models import (
    Model,
    CharField,
    DateTimeField
)

class Key(Model):
    api_key = CharField(
        max_length=30,
        null=False,
        blank=True,
        unique=True
    )

    created_at = DateTimeField(
        auto_now_add=True
    )

    class Meta:
        app_label = 'apikey'
        db_table = 'keys'
        ordering = [
            'api_key', 'created_at'
        ]
        
    def to_json(self):
        return {
            'api_key': self.api_key,
            'created_at': self.created_at
        }