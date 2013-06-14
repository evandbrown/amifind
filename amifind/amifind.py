import boto.ec2

import exceptions
import amifilter
import util
import searchresult
import mappings

def find(f):
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
            print "got region %s" % region_name
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
        
        # If images were returned for the region
        if result[region.name] is not None and len(result[region.name]) > 0:
            # FILTER: Apply regular expression filters (AMIRegexFilter objects) to
            # list of boto.ec2.image.Image returned by EC2 API
            for re_filter in f.re_filters:
                result[region.name] = util.filter_object_list(
                                                            result[region.name],
                                                            re_filter.ami_attribute,
                                                            re_filter.re_string
                )
                
            # SORT: If the filter defines a sort, apply it
            if f.sorter:
                result[region.name] = util.sort_object_list(
                                                            result[region.name],
                                                            f.sorter.ami_attribute,
                                                            f.sorter.descending
                )

            # JUST_ONE: If filter should return just one image, do that here
            if f.just_one:
                result[region.name] = [result[region.name][mappings.just_one[f.just_one]]]

    return searchresult.SearchResult(result)

def amazon_linux_ebs_64_pv_latest(regions=None):
    """
    Find the latest Amazon Linux AMIS
    
    :param regions: Optional list of region strings (e.g., ['us-east-1', 'us-west-2']) to search. Defaults to all regions
    :type regions: list
    """
    regions = regions if regions else get_all_regions()
    f = Filters.LINUX_AMAZON_64_PV_EBS_LATEST.with_regions(regions)
    
    return find(f)

def amazon_linux_ebs_64_pv(regions=None):
    """
    Find the latest Amazon Linux AMIS
    
    :param regions: Optional list of region strings (e.g., ['us-east-1', 'us-west-2']) to search. Defaults to all regions
    :type regions: list
    """
    regions = regions if regions else get_all_regions()
    f = Filters.LINUX_AMAZON_64_PV_EBS.with_regions(regions)
    
    return find(f)

def get_all_regions():
    """
    Return a list of all available regions for the EC2 API
    
    :rtype: list
    :return: A list of boto.regioninfo.RegionInfo
    """
    return [region.name for region in boto.ec2.regions()]
    
class Filters:
    """
    Some pre-defined search filters
    """
    LINUX_AMAZON_64_PV_EBS = amifilter.AMIFilter(owner='amazon', os='', regions=get_all_regions(),
                                arch='x86_64', virt_type='paravirtual', 
                                root_dev_type='ebs').with_re_filter('name', '^(?:(?!beta|rc).)*$').with_re_filter('description', '^(?:(?!beta|rc).)*$').with_re_filter('name', 'amzn-ami').with_sort('name', descending=True)
    LINUX_AMAZON_64_PV_EBS_LATEST = amifilter.AMIFilter(owner='amazon', os='', regions=get_all_regions(),
                                arch='x86_64', virt_type='paravirtual', 
                                root_dev_type='ebs', just_one='first').with_re_filter('name', '^(?:(?!beta|rc).)*$').with_re_filter('description', '^(?:(?!beta|rc).)*$').with_re_filter('name', 'amzn-ami').with_sort('name', descending=True)
