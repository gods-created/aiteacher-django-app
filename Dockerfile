FROM python:3
COPY . /app
WORKDIR /app
RUN chmod 777 -R /app/*
RUN chmod +x /app/*
RUN pip install -r requirements.txt
CMD ["/app/entrypoint.sh"]