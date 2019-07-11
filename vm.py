import common
import vpc


def getExternalIpName(context):
    prefix = context.properties['prefix']
    return prefix + 'external-ip'

def getNatIp(context):
    return '$(ref.%s.address)' % getExternalIpName(context)


def createExternalIp(context):
    """Creates the external IP"""
    if common.MY_DEBUG:
        print 'ENTER vm.createExternalIp'

    my_ip_name = getExternalIpName(context)
    my_region = context.properties['region']
    my_vpc_name = vpc.getNetworkName(context)

    ret = {
        'name': my_ip_name,
        'type': 'compute.v1.address',
        'properties': {
            'region': my_region
        },
        'metadata': {
            'dependsOn': [my_vpc_name]
        }
    }

    if common.MY_DEBUG:
        print 'EXIT vm.createExternalIp, ret: ' + str(ret)
    return ret


def createVM(context):
    """Creates the VM"""
    if common.MY_DEBUG:
        print 'ENTER vpc.createVM'

    prefix = context.properties['prefix']
    my_vm_name = prefix + 'app-vm'
    my_zone = context.properties['zone']
    my_machine_type = 'projects/{}/zones/{}/machineTypes/f1-micro'.format(context.env['project'], my_zone)
    my_ip_name = getExternalIpName(context)
    my_subnet_name = vpc.getSubnetworkName(context)
    source_image = context.properties['source_image']
    # See: https://cloud.google.com/compute/docs/instances/adding-removing-ssh-keys
    public_key = context.properties['public_key']

    ret = {
        'name': my_vm_name,
        'type': 'compute.v1.instance',
        'properties': {
            'machineType': my_machine_type,
            'zone': my_zone,
            'disks': [{
                'boot': True,
                'type': 'PERSISTENT',
                'autoDelete': True,
                'mode': 'READ_WRITE',
                'deviceName': 'boot',
                'initializeParams': {
                    'sourceImage': source_image
                }
            }],
            'networkInterfaces': [{
                'subnetwork': '$(ref.%s.selfLink)' % my_subnet_name,
                'accessConfigs': [{
                    'natIP': getNatIp(context)

                }]
            }],
            'metadata': {
                'items': [
                    {
                        'key': 'ssh-keys',
                        'value': 'user:' + public_key
                    }
                ]
            }
        },
        'metadata': {
            'dependsOn': [my_ip_name]
        }
    }

    if common.MY_DEBUG:
        print 'EXIT vm.createVM, ret: ' + str(ret)
    return ret


def getResource(context):
    """Creates the VM"""
    if common.MY_DEBUG:
        print 'ENTER vm.getResource'
        print 'context: ' + str(context)

    vm = createVM(context)
    ip = createExternalIp(context)
    ret = [ip, vm]

    if common.MY_DEBUG:
        print 'EXIT vm.getResource'
        print 'ret: ' + str(ret)
    return ret
