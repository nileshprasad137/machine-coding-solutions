FROM python:3.11-alpine
LABEL maintainer="nileshprasad137@gmail.com"
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5001
CMD [ "python3", "server.py"]