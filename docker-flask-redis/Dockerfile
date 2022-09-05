# this is an official Python runtime, used as the parent image
FROM python:3

RUN mkdir /app

WORKDIR /app

# add the current directory to the container as /app
ADD . /app

# execute everyone's favorite pip command, pip install -r
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# unblock port 5000 for the Flask app to run on
EXPOSE 5001

# execute the Flask app
CMD ["python", "app.py"]
