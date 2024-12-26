#!/bin/sh

python manage.py runserver 0.0.0.0:8001 & \
python -m celery -A ai.tasks.send_answer:app worker --concurrency=4 --queues=high_priority