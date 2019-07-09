# Adapted from:
# https://github.com/GoogleCloudPlatform/deploymentmanager-samples/tree/master/examples/v2/project_creation
import sys
from apis import ApiResourceName

def GenerateConfig(context):
  """Generates config."""

  # Admin parent project in deployment.yaml.
  project_id = context.env['name']
  billing_name = 'billing_' + project_id

  if not (('organization-id' in context.properties) or ('parent-folder-id' in context.properties)):
    sys.exit('You must specify at least one of organization id or parent folder id')
  if not 'billing-account-name' in context.properties:
    sys.exit(('Missing billing-account-name'))

  parent_type = ''
  parent_id = ''
  if 'parent-folder-id' in context.properties:
    parent_type = 'folder'
    parent_id = context.properties['parent-folder-id']
  else:
    parent_type = 'organization'
    parent_id = context.properties['organization-id']

  project_id = ''
  project_name = ''
  if 'project-id' in context.properties:
    project_id = context.properties['project-id']
  else:
    sys.exit(('Missing project-id'))
  if 'project-name' in context.properties:
    project_name = context.properties['project-name']
  else:
    sys.exit(('Missing project-name'))

  resources = [{
      'name': project_id,
      'type': 'cloudresourcemanager.v1.project',
      'properties': {
          'name': project_name,
          'projectId': project_id,
          'parent': {
              'type': parent_type,
              'id': parent_id
          }
      }
  }, {
      'name': billing_name,
      'type': 'deploymentmanager.v2.virtual.projectBillingInfo',
      'metadata': {
          'dependsOn': [project_id]
      },
      'properties': {
          'name': 'projects/' + project_id,
          'billingAccountName': context.properties['billing-account-name']
      }
  }, {
      'name': 'apis',
      'type': 'apis.py',
      'properties': {
          'project': project_id,
          'billing': billing_name,
          'apis': context.properties['apis'],
          'concurrent_api_activation':
              context.properties['concurrent_api_activation']
      }
  }]
  return {'resources': resources}

