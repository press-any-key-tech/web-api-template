#!/bin/bash

# Configuration
GITHUB_TOKEN="YOUR_GITHUB_TOKEN"
OWNER="your_github_username_or_org"
REPO="your_repository_name"

# List of environments
ENVIRONMENTS=("dev" "pre" "pro")

# List of variables (name, value)
VARIABLES=(
  "VAR1=value1"
  "VAR2=value2"
)

# List of secrets (name, value)
SECRETS=(
  "SECRET1=secret_value1"
  "SECRET2=secret_value2"
)

# Function to create an environment
create_environment() {
  local environment=$1
  curl -X PUT \
    -H "Authorization: token $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github.v3+json" \
    "https://api.github.com/repos/$OWNER/$REPO/environments/$environment"
}

# Function to create a variable in an environment
create_variable() {
  local environment=$1
  local name=$2
  local value=$3
  curl -X PUT \
    -H "Authorization: token $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github.v3+json" \
    -d "{\"value\": \"$value\"}" \
    "https://api.github.com/repos/$OWNER/$REPO/environments/$environment/variables/$name"
}

# Function to encrypt a secret
encrypt_secret() {
  local public_key=$1
  local secret_value=$2
  echo -n "$secret_value" | openssl rsautl -encrypt -pubin -inkey <(echo "$public_key") | base64
}

# Function to create a secret in an environment
create_secret() {
  local environment=$1
  local name=$2
  local value=$3

  # Get the public key of the repository
  response=$(curl -s -H "Authorization: token $GITHUB_TOKEN" -H "Accept: application/vnd.github.v3+json" "https://api.github.com/repos/$OWNER/$REPO/actions/secrets/public-key")
  public_key=$(echo "$response" | jq -r .key)
  key_id=$(echo "$response" | jq -r .key_id)

  # Encrypt the secret value
  encrypted_value=$(encrypt_secret "$public_key" "$value")

  # Create the secret
  curl -X PUT \
    -H "Authorization: token $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github.v3+json" \
    -d "{\"encrypted_value\": \"$encrypted_value\", \"key_id\": \"$key_id\"}" \
    "https://api.github.com/repos/$OWNER/$REPO/environments/$environment/secrets/$name"
}

# Create environments and their variables and secrets
for environment in "${ENVIRONMENTS[@]}"; do
  echo "Creating environment: $environment"
  create_environment "$environment"

  for variable in "${VARIABLES[@]}"; do
    IFS='=' read -r name value <<< "$variable"
    echo "Creating variable: $name with value: $value in environment: $environment"
    create_variable "$environment" "$name" "$value"
  done

  for secret in "${SECRETS[@]}"; do
    IFS='=' read -r name value <<< "$secret"
    echo "Creating secret: $name in environment: $environment"
    create_secret "$environment" "$name" "$value"
  done
done