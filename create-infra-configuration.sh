#!/usr/bin/env bash

echo "First source the environment variables in ~/.gcp/"

if [ $# -ne 0 ]
then
  echo "Usage: ./create-infra-configuration.sh"
  exit 1
fi

# Create gcloud configuration for infra project.
echo "*** Creating gcloud configuration... ***"
gcloud config configurations create $VAR_INFRA_PROJ_ID
gcloud config set compute/region $VAR_REGION
gcloud config set compute/zone $VAR_ZONE
gcloud config set account $VAR_ACCOUNT
gcloud config set project $VAR_INFRA_PROJ_ID
gcloud config configurations list
gcloud config get-value project
