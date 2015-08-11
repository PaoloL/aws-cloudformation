#!/bin/sh

environment=$1
tier=$2
name=$3

if [ -z "$environment" ]; then
  echo "environment not set";
  exit 1;
fi;

if [ -z "$tier" ]; then
  echo "tier not set";
  exit 1;
fi;

if [ -z "$name" ]; then
    name=1
fi;

echo "Creating $environment stack $name for $tier tier"

env $(cat .env | xargs) aws cloudformation create-stack \
    --stack-name demo-$tier-$environment-$name  \
    --region us-east-1 \
    --capabilities="CAPABILITY_IAM" \
    --template-body file://./cloudformation/$tier/$tier.json \
    --parameters file://./cloudformation/$tier/$environment.json \
    --profile xpeppers-lab
