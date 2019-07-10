import common


def createNetwork(context):
    if common.MY_DEBUG:
        print 'ENTER vpc.createNetwork'

    prefix = context.properties['prefix']
    my_vpc_name = prefix + 'vpc'

    ret = {
        'name': my_vpc_name,
        'type': 'compute.v1.network',
        'properties': {
            'routingConfig': {
                'routingMode': 'REGIONAL'
            },
            'autoCreateSubnetworks': False
        }
    }
    if common.MY_DEBUG:
        print 'EXIT vpc.createNetwork, ret: ' + str(ret)
    return ret

def createSubnet(context):
    if common.MY_DEBUG:
        print 'ENTER vpc.createSubnet'

    prefix = context.properties['prefix']
    my_vpc_name = prefix + 'vpc'

    prefix = context.properties['prefix']
    my_vpc_name = prefix + 'vpc'
    my_subnet_name = prefix + 'app-subnet'
    my_region = context.properties['region']
    my_cidr = context.properties['ipCidrRange']

    ret = {
        'name': my_subnet_name,
        'type': 'compute.v1.subnetwork',
        'properties': {
            'name': my_subnet_name,
            'network': '$(ref.%s.selfLink)' % my_vpc_name,
            'region': my_region,
            'ipCidrRange': my_cidr
        },
        'metadata': {
            'dependsOn': [my_vpc_name]
        }
    }

    if common.MY_DEBUG:
        print 'EXIT vpc.createSubnet, ret: ' + str(ret)
    return ret


def getResource(context):
    """Creates the vpc (network)."""
    if common.MY_DEBUG:
        print 'ENTER vpc.getResource'
        print 'context: ' + str(context)

    network = createNetwork(context)
    subnet = createSubnet(context)
    ret = [network, subnet]

    if common.MY_DEBUG:
        print 'EXIT vpc.getResource'
        print 'ret: ' + str(ret)
    return ret
