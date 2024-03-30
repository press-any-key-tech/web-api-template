FROM python:3.12 AS requirements-stage

ARG package_name=web_api_template
ARG module_name=web_api_template

# Create structure and install poetry
WORKDIR /tmp
RUN mkdir projects
RUN pip install poetry

# Build requirements
COPY ./pyproject.toml ./poetry.lock* ./projects/${package_name}/
RUN cd projects/${package_name} && poetry export -f requirements.txt --output requirements.txt --without-hashes

# ---------------------------------

# Build execution container
FROM python:3.12-alpine

# ARGs are needed in all the stages
ARG package_name=web_api_template
ARG module_name=web_api_template

# Install additional libraries
RUN apk add --no-cache curl-dev

ENV PORT 8000

EXPOSE 8000/tcp
EXPOSE 80/tcp

WORKDIR /code

# Install requirements
COPY --from=requirements-stage /tmp/projects/${package_name}/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code

CMD ["sh", "-c", "uvicorn web_api_template.main:app --host 0.0.0.0 --port $PORT"]
