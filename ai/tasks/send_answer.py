from os import environ
from celery import Celery
from loguru import logger
from django.core.mail import send_mail
from minions import (
    get_answer,
)

environ.setdefault('DJANGO_SETTINGS_MODULE', 'aiteacher.settings')
app = Celery('send_answer', broker='redis://localhost:6379')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.task_queues = {
    'high_priority': {
        'exchange': 'high_priority',
        'routing_key': 'high.#'
    }
}

@app.task
def send_answer(*args, **kwargs):
    try:
        email, question = kwargs.get('email'), kwargs.get('question')
        answer = get_answer(question)

        send_mail(
            'Answer question from AI',
            f'Answer: \'{answer}\'',
            'tersk.bo@gmail.com',
            [
                email,
            ],
            fail_silently=False,
        )
        
    except (Exception, ) as e:
        logger.error(f'\'send_answer\' task error: \'{str(e)}\'')