FROM python:3.12-slim


#set working directory
WORKDIR /app


#set poetry
RUN pip install poetry
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry config virtualenvs.create false && poetry install --no-root

#copy project files
COPY . .

#port
EXPOSE 8000

#run command
# CMD ["python", "mysite/manage.py", "runserver", "127.0.0.1:8000"]
WORKDIR /app/mysite
CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000"]


# build docker image
# docker build -t blogproject .
# docker run -p 8000:8000 blogproject