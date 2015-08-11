#!/bin/sh

project=$1
environment=$2
tier=$3
name=$4

if [ -z "$project" ]; then
  echo "project not set";
  exit 1;
fi;

if [ -z "$environment" ]; then
  echo "environment not set";
  exit 1;
fi;

if [ -z "$tier" ]; then
  echo "tier not set";
  exit 1;
fi;

if [ -z "$name" ]; then
    name="General"
fi;

echo "Creating $environment stack $name for $tier tier"

env $(cat .env | xargs) aws cloudformation create-stack \
    --stack-name $project-$environment-$tier-$name  \
    --region eu-west-1 \
    --capabilities="CAPABILITY_IAM" \
    --template-body file://./cloudformation/$tier/$tier.json \
    --parameters file://./cloudformation/$tier/$environment.json \
    --profile proDemo-provisioning
