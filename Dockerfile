FROM python:3.9
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
# ARG MONGO_API_KEY
# ENV MONGO_API_KEY=$MONGO_API_KEY
# ARG CSRF_KEY
# ENV CSRF_KEY=$CSRF_KEY
# ARG JWT_KEY
# ENV JWT_KEY=$JWT_KEY
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]