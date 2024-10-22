FROM python:3.8
LABEL maintainer="noemail@website.domain"
RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["flask_maps.py"]
