ARG PYTHON_IMAGE=python:3.12.6-alpine3.20
FROM $PYTHON_IMAGE AS dependencies-build


# Install packages
RUN apk add --no-cache libcurl

# Needed for pycurl
ENV PYCURL_SSL_LIBRARY=openssl
RUN  apk add --no-cache postgresql-libs && \
       apk add curl --no-cache && \
       apk add htop --no-cache && \
       apk add vim vim-doc vim-tutor --no-cache && \
       apk add curl-dev --no-cache && \
       apk add bash --no-cache && \
       apk add linux-headers --no-cache && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev
RUN apk upgrade --no-cache

WORKDIR /
COPY migrations /app/migrations
COPY src /app/src
COPY requirements.txt /app/requirements.txt
COPY alembic.ini /app/alembic.ini
COPY main.py /app/main.py

ARG MYDIR=/app
WORKDIR $MYDIR

RUN pip install -r requirements.txt

# WORKDIR $MYDIR

ENV PATH="/home/appuser/.local/bin:${PATH}"

FROM dependencies-build AS run-tests
ARG MYDIR=/app

COPY --from=dependencies-build /app /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY --chown=appuser:appuser tests /app/tests
COPY --chown=appuser:appuser .flake8 /app/.flake8
WORKDIR $MYDIR

# RUN python -m flake8
# RUN bandit -r src/
RUN python -m pytest --cov=src --cov-report=xml tests
# ENTRYPOINT ["python", "main.py", "server"]