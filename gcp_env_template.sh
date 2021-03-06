#!/bin/bash

echo "Use source!"
echo "You have to use unique IDs for project. In GCP any project id that has ever been used cannot be used again! Use GCP_DEPL_VERSION to define new unique id."

export GCP_INFRA_VERSION=<GIVE-YOUR-UNIQUE-NUMBER>

# Max 30 chars lenght.
export VAR_INFRA_PROJ_ID=<GIVE-INFRA-PROJECT-ID>-id-$GCP_INFRA_VERSION
export VAR_INFRA_PROJ_NAME=<GIVE-INFRA-PROJECT-NAME>
export VAR_FOLDER_ID=<GIVE-FOLDER-ID>
export VAR_ORG_ID=<GIVE-ORGANIZATION-ID>
export VAR_BILLING_ACCOUNT_ID=<GIVE-BILLING-ACCOUNT-ID>
export VAR_REGION=<GIVE-REGION>
export VAR_ZONE=<GIVE-ZONE>
export VAR_ACCOUNT=<GIVE-ACCOUNT>

echo "VAR_INFRA_PROJ_ID: $VAR_INFRA_PROJ_ID"
echo "VAR_INFRA_PROJ_NAME: $VAR_INFRA_PROJ_NAME"
echo "VAR_CONFIG_NAME: $VAR_CONFIG_NAME"
# Do not list these in demos:
#echo "VAR_FOLDER_ID: $VAR_FOLDER_ID"
#echo "VAR_ORG_ID: $VAR_ORG_ID"
#echo "VAR_BILLING_ACCOUNT_ID: $VAR_BILLING_ACCOUNT_ID"

#echo "List configurations:"
#gcloud config configurations list

