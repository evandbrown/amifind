class AMIFilter(object):
    def __init__(self, owner, regions=None, os=None, arch=None,
                 virt_type=None, root_dev_type=None):
        """
        Initialize a new AMIFilter. Only region and owner are required. 
        """
        self.owner = owner
        self.regions = regions
        self.os = os
        self.arch = arch
        self.virt_type = virt_type
        self.root_dev_type = root_dev_type
    
    def get_ec2_api_filter(self):
        """
        Return an EC2 API-compatible string that can be used
        to filter tbe EC2->DescribeImages API
        """
        filters = {}
        filters['owner-alias'] = self.owner
        return filters
        
    def is_complete(self):
        """
        Return true if this filter has all of the necessary values to
        locate a single AMI
        """
        return (self.regions and self.owner and self.os and self.arch and self.virt_type and self.root_dev_type)
        