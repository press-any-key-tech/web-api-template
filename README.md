# web-api-template

Python template for web API projects

## Technology Stack:

- FastAPI
- Uvicorn (server)
- Pytest (\*)
- PostgreSql

## Development environment

### Requirements:

- Docker CE (Linux) or Docker Desktop (MacOS, Windows).
- Python >= 3.12 (Pyenv, best option)
- Poetry as dependency manager

### Activate development environment

```
poetry install
```

This will create a new virtual environment (if it does not exists) and will install all the dependencies.

To activate the virtual environment use:

```
poetry shell
```

### Add/remove dependencies

```
poetry add PIP_PACKAGE [-G group.name]
```

Add dependency to the given group. If not specified will be added to the default group.

```
poetry remove PIP_PACKAGE [-G group.name]
```

Remove dependency from the given group

### Run project from command line

Set, at least, the SQLALCHEMY_DATABASE_URI environment variable

```
cd src/web_api_template
poetry run python -m uvicorn main:app --reload --port 8000
```

### Debug project from VS Code

First create a .env file in the root folder or copy the existing .env.example and set the SQLALCHEMY_DATABASE_URI and the CORS_ALLOWED_ORIGINS variables.

Then use the Launch option from Visual Studio Code

## Tests

### Debug From VS Code

Get the path of the virtual environment created by poetry:

```bash
poetry env info -p
```

Set in visual studio code the default interpreter to the virtual environment created by poetry.(SHIT+CTRL+P Select interpreter)

Launch "Pytest launch" from the run/debug tab.

You can set breakpoints and inspections

### Launch tests from command line

```
poetry run pytest --cov-report term-missing --cov=web_api_template ./tests
```

This will launch tests and creates a code coverage report.

### Exclude code from coverage

When you need to exclude code from the code coverage report set, in the lines or function to be excluded, the line:

```
# pragma: no cover
```

See: https://coverage.readthedocs.io/en/6.4.4/excluding.html

## Docker build and run

### Build

From root directory execute:

```bash
docker build -f ./docker/Dockerfile.api -t web-api-template .
```

### Run

From root directory execute:

```bash
docker run -d --name web_api_template -p 8000:8000 -e SQLALCHEMY_DATABASE_URI='postgresql+asyncpg://test:test123@LOCAL_SERVER_IP:5432/mytemplate' web-api-template
```

Do not use "localhost" as LOCAL_SERVER_IP, use your local IP address instead. Docker container will not be able to connect to your local database otherwise.

## Data support services

### Postgresql and Redis

From root directory execute:

```
docker-compose -f docker-compose-db.yaml up -d
```

OR

Use -p flag to specify an alternative project name instead of the directory name. This is useful if you have multiple projects running on a single host.

```
docker-compose -f docker-compose-db.yaml -p my-web-api-template up -d
```

### Localstack (Dynamodb and SQS)

From root directory execute:

```
docker-compose -f docker-compose-localstack.yaml up -d
```

OR

Use -p flag to specify an alternative project name instead of the directory name. This is useful if you have multiple projects running on a single host.

```
docker-compose -f docker-compose-localstack.yaml -p my-web-api-template up -d
```

### Stop

From root directory execute:

```
docker-compose -f docker-compose-db.yaml down
```

OR

Use -p flag to specify an alternative project name instead of the directory name. This is useful if you have multiple projects running on a single host.

```
docker-compose -f docker-compose-db.yaml -p my-web-api-template down
```

## Complete Development services

Start databases and API services in one go.

### Start

From root directory execute:

```
docker-compose -f docker-compose.yaml up -d
```

OR

Use -p flag to specify an alternative project name instead of the directory name. This is useful if you have multiple projects running on a single host.

```
docker-compose -f docker-compose.yaml -p my-web-api-template up -d
```

### Start rebuilding images

From root directory execute:

```
docker-compose -f docker-compose.yaml up -d --build
```

### Stop

From root directory execute:

```
docker-compose -f docker-compose.yaml down
```

OR

Use -p flag to specify an alternative project name instead of the directory name. This is useful if you have multiple projects running on a single host.

```
docker-compose -f docker-compose.yaml -p my-web-api-template down
```

## IaC

### Create bucket on AWS

Create a bucket to keep status files.

```
aws --profile pak s3api create-bucket --bucket web-api-template-devops01 --region eu-west-1 --create-bucket-configuration LocationConstraint=eu-west-1
```

### Configure provider on Terraform

After that, execute terraform init

```
terraform init --backend-config=../application.dev.backend.conf -reconfigure
```

### Apply/destroy infrastructure

```
terraform apply --var-file="../configuration.application.dev.tfvars"
```

## Cognito

### Login URL

https://web-api-template-domain.auth.eu-west-1.amazoncognito.com/oauth2/authorize?client_id=5p6vlnt8u8s1l1b6b7hc2vnulv&response_type=token&scope=email+openid+phone+profile&redirect_uri=http%3A%2F%2Flocalhost%3A4200

### Logout URL

https://web-api-template-domain.auth.eu-west-1.amazoncognito.com/logout?client_id=5p6vlnt8u8s1l1b6b7hc2vnulv&response_type=token&redirect_uri=http%3A%2F%2Flocalhost%3A4200

### API login

Login using client id and secret

POST to: https://web-api-template-domain.auth.eu-west-1.amazoncognito.com/oauth2/token

Body:
grant_type client_credentials
client_id ...
client_secret

Body type x-www-form-urlencoded

Headers: Content-Type application/x-www-form-urlencoded
