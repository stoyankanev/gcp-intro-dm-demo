# Adapted from:
# https://github.com/GoogleCloudPlatform/deploymentmanager-samples/tree/master/examples/v2/project_creation


def GenerateConfig(context):
  """Generates config."""

  project_id = context.properties['project']
  billing = context.properties['billing']
  concurrent_api_activation = context.properties['concurrent_api_activation']

  resources = []
  for index, api in enumerate(context.properties['apis']):
    depends_on = [project_id, billing]
    # Serialize the activation of all the apis by making api_n depend on api_n-1
    if (not concurrent_api_activation) and index != 0:
      depends_on.append(
          ApiResourceName(project_id, context.properties['apis'][index-1]))
    resources.append({
        'name': ApiResourceName(project_id, api),
        'type': 'deploymentmanager.v2.virtual.enableService',
        'metadata': {
            'dependsOn': depends_on
        },
        'properties': {
            'consumerId': 'project:' + project_id,
            'serviceName': api
        }
    })
  return {'resources': resources}


def ApiResourceName(project_id, api_name):
  return project_id + '-' + api_name
