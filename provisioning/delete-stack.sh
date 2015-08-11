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

echo "Deleting $environment stack $name for $tier tier"

env $(cat .env | xargs) aws cloudformation delete-stack --stack-name $project-$environment-$tier-$name --profile preDemo-superprovisioning
