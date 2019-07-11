import common


def getNetworkName(context):
    prefix = context.properties['prefix']
    return prefix + 'vpc'


def getSubnetworkName(context):
    prefix = context.properties['prefix']
    return prefix + 'app-subnetwork'


def createNetwork(context):
    """Creates the vpc (network)."""
    if common.MY_DEBUG:
        print 'ENTER vpc.createNetwork'

    my_vpc_name = getNetworkName(context)

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
    """Creates the subnet."""
    if common.MY_DEBUG:
        print 'ENTER vpc.createSubnet'

    prefix = context.properties['prefix']
    my_vpc_name = getNetworkName(context)
    my_subnet_name = getSubnetworkName(context)
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


def createFirewall(context):
    """Creates the firewall."""
    if common.MY_DEBUG:
        print 'ENTER vpc.createFirewall'

    prefix = context.properties['prefix']
    my_vpc_name = getNetworkName(context)
    my_firewall_name = prefix + 'app-firewall'

    ret = {
        'name': my_firewall_name,
        'type': 'compute.v1.firewall',
        'properties': {
            'network': '$(ref.%s.selfLink)' % my_vpc_name,
            'description': 'Allow SSH to app-subnetwork VM instances',
            'priority': 500,
            'direction': 'INGRESS',
            'sourceRanges': ['0.0.0.0/0'],
            'allowed': [{
                'IPProtocol': 'TCP',
                'ports': [22]
            },
                {
                    'IPProtocol': 'ICMP',
                }
            ]
        },
        'metadata': {
            'dependsOn': [my_vpc_name]
        }
    }

    if common.MY_DEBUG:
        print 'EXIT vpc.createFirewall, ret: ' + str(ret)
    return ret


def getResource(context):
    """Creates the vpc entities (vpc, subnet and firewall)."""
    if common.MY_DEBUG:
        print 'ENTER vpc.getResource'
        print 'context: ' + str(context)

    network = createNetwork(context)
    subnet = createSubnet(context)
    firewall = createFirewall(context)
    ret = [network, subnet, firewall]

    if common.MY_DEBUG:
        print 'EXIT vpc.getResource'
        print 'ret: ' + str(ret)
    return ret
