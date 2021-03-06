FROM python:3.7

# Setup the app structure in the container
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app

# Install requirements and run
RUN pip install -r requirements.txt
ADD . /app
CMD ["uwsgi","--http","0.0.0.0:5000","--module","app:app","--processes","2"]
