#!/usr/bin/env bash


if [ $# -ne 0 ]
then
  echo "Usage: ./create-deployment.sh"
  exit 1
fi


gcloud deployment-manager deployments create ${VAR_INFRA_PROJ_ID}-deployment --config deployment.yaml --project $VAR_ADMIN_PROJ_ID
#gcloud deployment-manager deployments create ${VAR_INFRA_PROJ_ID}-deployment --config deployment.yaml
