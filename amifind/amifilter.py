class AMIFilter(object):
    """
    This class defines a filter that is used to search for AMIs in the
    EC2 API. Facilities are provided for basic (i.e., exact-match) filtering
    at the API level, and more advanced regular expression matching 
    """
    def __init__(self, owner, regions, os=None, arch=None,
                 virt_type=None, root_dev_type=None, just_one=None):
        """
        Initialize a new AMIFilter. Only region and owner are required. These parameters
        are passed as filters directly to the EC2 API and are for exact matches only.
        For wildcard filtering, see the add_regex_filter() method of this class.
        
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
        
        :param just_one: If set, only return one result after applying all
                         filters and sorts. Valid values are 'first' or
                         'last', indicating which image to keep if there
                         are more than one in the result list.
                         
                         This is useful when searching for
                         the latest version of an AMI where there may be
                         multiple versions of the images with a date string
                         in their name. Sorting on 'name' descending and
                         selecting the first or last would return the most
                         recent
        :type just_one: string
        """
        self.owner = owner
        self.regions = regions
        self.os = os
        self.arch = arch
        self.virt_type = virt_type
        self.root_dev_type = root_dev_type
        self.just_one = just_one
        
        # Initialize a list of optional regular expression filters and that may
        # be applied (client-side) to images returned from the EC2 API call
        self.re_filters = []
        
        # An optional attribute to enable sorting the results of this filter
        self.sorter = None
    
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
    
    def with_re_filter(self, ami_attribute, re_string):
        """
        Add a regular expression filter that will be applied to the
        specified attribute (attr_to_filter) of the list AMIs returned
        by the EC2 API call. Filters are applied in the order they are
        added, and are applied to the AMI list retrieved from the 
        EC2 API
        
        :param ami_attribute: The attribute of each list item to apply filter to. Valid attributes contained in boto.ec2.image.Image
        :type ami_attribute: string
        
        :param re_string: Regular expression to apply on attr_to_filter
        :type re_string: string
        """
        self.re_filters.append(AMIRegexFilter(ami_attribute, re_string))
                    
        return self
        
    def with_sort(self, ami_attribute, descending=False):
        """
        Sort search results on the indicated AMI attribute.
        
        :param ami_attribute: The attribute of each list item to sort. Valid attributes contained in boto.ec2.image.Image
        :type ami_attribute: string
        
        :param descending: Sort in descending order
        :type descending: bool
        """
        self.sorter = AMISorter(ami_attribute, descending)
        
        return self
        
    def with_just_one(self, just_one):
        """
        Modify the just_one property of this object, indicating that just one image
        should be returned from this filter
        """
        self.just_one = just_one
        
        return self    
    
    def with_regions(self, region_names):
        """
        Modify the regions for this filter.
        
        :param region_names: The region names to merge or overwrite with
        :type region_names: list

        """
        self.regions = region_names
        
        return self
                    
    #todo: this really belongs in whatever object ends up handling search results
    def is_complete(self):
        """
        Indicate if this filter has all of the necessary values to
        locate a single AMI
        
        :rtype: bool
        :return: True if all filter options are set, false otherwise.
        """
        return (self.regions and self.owner and self.os and self.arch and self.virt_type and self.root_dev_type)
    

class AMIRegexFilter:
    """
    A Regular Expression filter defines a regular expression and the
    corresponding attribute/property that the filter should be applied
    to AMIs/Images returned by boto.
    """

    def __init__(self, ami_attribute, re_string):
        """
        :param ami_attribute: The attribute to apply the regex to. Must be a valid attribute in a boto.ec2.image.Image object
        :type ami_attribute: string
        
        :param re_string: The regular expression to apply
        :type re_string: string
        """
        self.ami_attribute = ami_attribute
        self.re_string = re_string
 
class AMISorter:
    """
    A simple sort definition, identifying an AMI filter
    to sort on, as well as direction of sort
    """

    def __init__(self, ami_attribute, descending=False):
        """
        :param ami_attribute: The attribute to apply the sort to. Must be a valid attribute in a boto.ec2.image.Image object
        :type ami_attribute: string
        
        :param descending: Sort in descending order
        :type descending: bool
        """
        self.ami_attribute = ami_attribute
        self.descending = descending