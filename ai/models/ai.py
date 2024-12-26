from django.db.models import (
    Model,
    TextField,
    EmailField,
    DateTimeField
)

class AIQuestionStore(Model):
    email = EmailField(
        null=False,
        blank=True,
        max_length=50
    )

    question = TextField(
        null=False,
        blank=True,
        max_length=1000
    )

    created_at = DateTimeField(
        auto_now_add=True
    )

    class Meta:
        app_label = 'ai'
        db_table = 'ai'
        ordering = [
            'question', 'created_at'
        ]