ARG PYTHON_IMAGE=python:3.12.6-alpine3.20
FROM $PYTHON_IMAGE AS dependencies-build


# Install packages
RUN apk add --no-cache libcurl

# Needed for pycurl
ENV PYCURL_SSL_LIBRARY=openssl
RUN  apk add --no-cache postgresql-libs && \
       apk add curl --no-cache && \
       apk add curl-dev --no-cache && \
       apk add bash --no-cache && \
       apk add linux-headers --no-cache && \
       apk add --no-cache --virtual .build-deps gcc musl-dev
RUN apk upgrade --no-cache

WORKDIR /
COPY ../gui /app

ARG MYDIR=/app
WORKDIR $MYDIR

RUN pip install -r requirements.txt

ENV PATH="/home/appuser/.local/bin:${PATH}"

# ENTRYPOINT ["streamlit", "run", "home.py"]