FROM python:3.7

# Create app directory
WORKDIR /master


# Bundle app source
COPY . /master

EXPOSE 8080
CMD [ "python3", "server.py" ]