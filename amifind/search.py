import boto.ec2

import exceptions
import amifilter

def search(amifilter):
    """ Search EC2 AMIs based on provided AMIFilter """
    
    # Build a list of connections, either one conne to the region
    # in the AMIFilter, or connections to all available regions
    # if no region was specified in the filter.
    regions = []
    if amifilter.regions is None:
        regions = get_all_regions()
    else:
        for region_name in amifilter.regions:
            region = boto.ec2.get_region(region_name)
            if region is None:
                raise exceptions.AMIFilterException("Invalid region: %s" % region_name)
            else:
                regions.append(region)

    # Iterate over every region, connecting to the EC2 API
    # there and retrieving images based on the filter
    images={}
    for region in regions:
        images[region.name] = region.connect().get_all_images(
                filters=amifilter.get_ec2_api_filter()
        )

    return images

def search_amazon_linux(regions=None):
    f = amifilter.AMIFilter(owner='amazon', regions=['us-west-2'], os='',
                            arch='x86_64', virt_type='paravirtual', 
                            root_dev_type='ebs')
    return search(f)

def connect_ec2(region_name):
    """ Get a connection to EC2 in the specified region """
    return boto.ec2.connect_to_region(region_name)
    
def get_all_regions():
    """ Return a list of all EC2 region names """
    return boto.ec2.regions()