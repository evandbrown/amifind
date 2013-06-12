import boto.ec2

import exceptions
import amifilter
import util
import searchresult

def with_filter(f):
    """
    Search EC2 AMIs based on provided filter
    
    :param f: AMIFilter to search on
    :type f: amifilter.AMIFilter
    
    :rtype: amifind.searchresult.SearchResult
    :return: A SearchResult object for the search performed with the filter
    """
    
    # Build a list of connections, either one conne to the region
    # in the f, or connections to all available regions
    # if no region was specified in the filter.
    regions = []
    if f.regions is None:
        regions = get_all_regions()
    else:
        # Iterate each region provided in the filter and get a 
        # region object from boto
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
        
        # Apply regular expression filters (AMIRegexFilter objects) to
        # list of boto.ec2.image.Image returned by EC2 API
        for re_filter in f.re_filters:
            result[region.name] = (util.filter_object_list(
                                                        result[region.name],
                                                        re_filter.ami_attribute,
                                                        re_filter.re_string
                                                        ))

    return searchresult.SearchResult(result)

def amazon_linux_ebs_64_pv_latest(regions=None):
    """
    Find the latest Amazon Linux AMIS
    
    :param regions: Optional list of region strings (e.g., ['us-east-1', 'us-west-2']) to search. Defaults to all regions
    :type regions: list
    """
    f = amifilter.Filters.LINUX_AMAZON_64_PV_EBS.with_regions(regions)
    f.add_re_filter('name', '^(?:(?!beta|rc).)*$')
    f.add_re_filter('description', '^(?:(?!beta|rc).)*$')
    
    return with_filter(f)
    
def get_all_regions():
    """
    Return a list of all available regions for the EC2 API
    
    :rtype: list
    :return: A list of boto.regioninfo.RegionInfo
    """
    return boto.ec2.regions()
    
    
