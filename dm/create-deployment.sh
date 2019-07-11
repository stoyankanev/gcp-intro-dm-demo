#!/usr/bin/env bash


if [ $# -ne 0 ]
then
  echo "Usage: ./create-deployment.sh"
  exit 1
fi

echo "First source your environment variables and edit deployment.yaml file! See README.md"
echo "Check in gcloud cli that you are using the right configuration: gcloud config configurations list"

gcloud deployment-manager deployments create ${VAR_INFRA_PROJ_ID}-deployment --config deployment.yaml --project $VAR_INFRA_PROJ_ID


