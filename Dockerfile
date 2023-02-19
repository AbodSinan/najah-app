FROM python:3.9-slim


# Docker arguments
ARG BUILD_TYPE
ARG COMMIT_HASH=untagged

RUN mkdir -p \
    /code/static/

WORKDIR /code/

RUN apt-get update && apt-get install -y \
   build-essential \
   python3-dev \
   mysql-devel \
   gcc

RUN pip3 install --upgrade pip && pip3 install poetry
COPY pyproject.toml poetry.lock /code/

SHELL ["/bin/bash", "-c"]
RUN poetry config virtualenvs.create false && \
    poetry install $([[ "$BUILD_TYPE" == prod* ]] && echo "--only main") --no-interaction

COPY . /code/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
