import boto.ec2

import exceptions
import amifilter
import util
import searchresult

def search_with_filter(f):
    """
    Search EC2 AMIs based on provided filter
    
    :param f: AMIFilter to search on
    :type f: amifilter.AMIFilter
    """
    
    # Build a list of connections, either one conne to the region
    # in the f, or connections to all available regions
    # if no region was specified in the filter.
    regions = []
    if f.regions is None:
        regions = get_all_regions()
    else:
        for region_name in f.regions:
            region = boto.ec2.get_region(region_name)
            if region is None:
                raise exceptions.AMIFilterException("Invalid region: %s" % region_name)
            else:
                regions.append(region)

    # Iterate over every region, connecting to the EC2 API
    # there and retrieving images based on the filter
    result={}
    for region in regions:
        # Retrieve AMI list from EC2 API, applying non-wildcard filters
        result[region.name] = region.connect().get_all_images(filters=f.get_ec2_api_filter())
        
        print "got %i amis. applying %i filters" % (len(result[region.name]), len(f.re_filters))
        
        # Apply regular expression filters
        for re_filter in f.re_filters:
            result[region.name] = (util.filter_object_list(result[region.name], re_filter['attribute'], re_filter['re_string']))

    return searchresult.SearchResult(result)

def find_amazon_linux_ebs_64_pv_latest(regions=None):
    """
    Find the latest Amazon Linux AMIS
    
    :param regions: Optional list of region strings (e.g., ['us-east-1', 'us-west-2']) to search. Defaults to all regions
    :type regions: list
    """
    f = amifilter.Filters.LINUX_AMAZON_64_PV_EBS.with_region('us-west-2')
    f.add_re_filter('name', '^(?:(?!beta|rc).)*$')
    f.add_re_filter('description', '^(?:(?!beta|rc).)*$')
    
    return search_with_filter(f)

def connect_ec2(region_name):
    """ Get a connection to EC2 in the specified region """
    return boto.ec2.connect_to_region(region_name)
    
def get_all_regions():
    """ Return a list of all EC2 region names """
    return boto.ec2.regions()
    
    
