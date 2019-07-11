import yaml
import deployment

"""This file is just for local testing."""

MY_DEBUG = True
MY_DEPLOYMENT_YAML='deployment.yaml'

class Object(object):
    pass

def simulateContext():
    """Reads the deployment.yaml properties, thus simulating real context."""
    stream = file(MY_DEPLOYMENT_YAML, 'r')
    dict = yaml.safe_load(stream)
    props = dict['resources'][0]['properties']
    context = Object()
    context.properties = props
    env = {'project': 'foo'}
    context.env = env

    return context

def main():
    test_config = {}
    if MY_DEBUG:
        print 'ENTER mymain.main'
    context = simulateContext()
    print 'context: ' + str(context)
    resources = deployment.GenerateConfig(context)
    print 'resources: ' + str(resources)
    if MY_DEBUG:
        print 'EXIT mymain.main'

if __name__ == "__main__":
    main()

