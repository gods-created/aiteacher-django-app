# AITeacher

## Overview
AITeacher allows you to train AI models or get answers from the models delivered directly to your email. You can obtain an API key and access the API documentation at `/api/docs`. A pre-configured Docker container is available to simplify the setup process.

---

## Local Launch Instructions

### Prerequisites
Ensure you have the following installed:
- [Redis](https://redis.io/download)
- [Python](https://www.python.org/downloads/) (compatible version)
- [Brew (macOS)](https://brew.sh/) for package management

### Steps
1. **Install and start Redis:**
    ```bash
    brew install redis
    brew services start redis
    redis-cli
    ```

2. **Set up the project:**
    ```bash
    cd /aiteacher
    python -m pip install -r requirements.txt
    ```

3. **Apply migrations:**
    ```bash
    python manage.py makemigrations ai
    python manage.py migrate ai --database='ai'

    python manage.py makemigrations apikey
    python manage.py migrate apikey --database='keys'
    ```

4. **Run the server and Celery worker:**
    ```bash
    python manage.py runserver localhost:8001 & \
    python -m celery -A ai.tasks.send_answer:app worker --concurrency=4 --queues=high_priority
    ```

---

## Docker Launch Instructions

### Prerequisites
Ensure Docker and Docker Compose are installed on your system. You can download them from the [Docker website](https://www.docker.com/).

### Steps
1. **Launch the application:**
    ```bash
    docker-compose up && docker-compose run
    ```

---

## Additional Information
- Access the API documentation at: `/api/docs`
- Don't forget create .env file or edit env in docker-compose.yml and broker in celery task if using docker