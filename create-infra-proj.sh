#!/usr/bin/env bash


if [ $# -ne 0 ]
then
  echo "Usage: ./create-infra-proj.sh"
  exit 1
fi


# Create infra project.
echo "*** Creating infra project... ***"
gcloud projects create $VAR_INFRA_PROJ_ID --folder=$VAR_FOLDER_ID --name=$VAR_INFRA_PROJ_NAME

# Create gcloud configuration for infra project.
echo "*** Creating gcloud configuration... ***"
gcloud config configurations create $VAR_INFRA_PROJ_ID
gcloud config set compute/region $VAR_REGION
gcloud config set compute/zone $VAR_ZONE
gcloud config set account $VAR_ACCOUNT
gcloud config set project $VAR_INFRA_PROJ_ID
gcloud config configurations list
gcloud config get-value project
# Assign billing account
#gcloud beta billing accounts list
gcloud beta billing projects link $VAR_INFRA_PROJ_ID --billing-account $VAR_BILLING_ACCOUNT_ID
echo "Turning services on..."
sleep 2
# Needing these for deployments since we are using the same project for deployments (see README).
gcloud services enable deploymentmanager.googleapis.com
gcloud services enable cloudresourcemanager.googleapis.com
gcloud services enable cloudbilling.googleapis.com
gcloud services enable iam.googleapis.com
gcloud services enable servicemanagement.googleapis.com
# Needing these for actual infra resources (VM).
gcloud services enable oslogin.googleapis.com
gcloud services enable compute.googleapis.com

