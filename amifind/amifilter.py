class AMIFilter(object):
    def __init__(self, owner, regions=None, os=None, arch=None,
                 virt_type=None, root_dev_type=None):
        """
        Initialize a new AMIFilter. Only region and owner are required.
        
        :param owner: Owner alias of AMIs to search for
        :type owner: string
        
        :param regions: EC2 Regions to search
        :type regions: list
        
        :param os: Operating System. Valid values: windows, linux
        :type os: string
        
        :param arch: Architecture. Valid values: i386, x86_64
        :type arch: string
        
        :param virt_type: Virtualization type. Valid values: paravirtual, hvm
        :type virt_type: string
        
        :param root_dev_type: Root device type. Valid values: ebs, instance-store
        :type root_dev_type: string
        """
        self.owner = owner
        self.regions = regions
        self.os = os
        self.arch = arch
        self.virt_type = virt_type
        self.root_dev_type = root_dev_type
    
    def get_ec2_api_filter(self):
        """
        Create EC2 API-compatible string that can be used
        to filter with tbe EC2->DescribeImages API
        
        :rtype: dict
        :return: A dictionary of EC2 API-compatible filters
        """
        filters = {}
        filters['owner-alias'] = self.owner
        
        if self.os:
            filters['platform'] = self.os
            
        if self.arch:
            filters['architecture'] = self.arch
            
        if self.virt_type:
            filters['virtualization-type'] = self.virt_type
            
        if self.root_dev_type:
            filters['root-device-type'] = self.root_dev_type
            
        return filters
        
    def is_complete(self):
        """
        Indicate if this filter has all of the necessary values to
        locate a single AMI
        
        :rtype: bool
        :return: True if all filter options are set, false otherwise.
        """
        return (self.regions and self.owner and self.os and self.arch and self.virt_type and self.root_dev_type)
    
    
    operating_systems = {
        'Windows': 'windows',
        'windows': 'windows',
        'linux': 'linux'
    }
    """ Supported values for os filter """
    
    architectures = {
        '32': 'i386',
        'i386': 'i386',
        '64': 'x86_64',
        'x86_64': 'x86_64'
    }
    """ Supported values for arch filter"""
    
    virtualization_types = {
        'hvm': 'hvm',
        'pv': 'paravirtual',
        'paravirtual': 'paravirtual'
    }
    """ Supported values for virt_type filter """
    
    root_device_types = {
        'ebs': 'ebs',
        's3': 'instance-store',
        'instance-store': 'instance-store'
    }
    """ Supported values for root_dev_type """
    