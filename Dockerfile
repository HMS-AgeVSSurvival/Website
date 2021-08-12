FROM python:3.9.5-buster

RUN mkdir /website
WORKDIR /website

COPY . .

RUN pip install -e .

CMD exec gunicorn --bind 0.0.0.0:8080 'website.index:get_server()'

# docker build -t gcr.io/agevssurvival-317113/website .
# docker run -p 8080:8080 gcr.io/agevssurvival-317113/website
# docker push gcr.io/agevssurvival-317113/website