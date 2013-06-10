import boto.ec2

def search(amifilter):
    """ Search EC2 AMIs based on provided AMIFilter """
    
    # Build a list of connections, either one conne to the region
    # in the AMIFilter, or connections to all available regions
    # if no region was specified in the filter.
    regions = []
    if amifilter.regions is None:
        regions = get_all_regions()
    else:
        regions = amifilter.regions

    # Iterate over every region, connecting to the EC2 API
    # there and retrieving images based on the filter
    images={}
    for region in regions:
        images[region] = connect_ec2(region).get_all_images(
                filters=amifilter.get_ec2_api_filter()
        )

    return images

def connect_ec2(region_name):
    """ Get a connection to EC2 in the specified region """
    return boto.ec2.connect_to_region(region_name)
    
def get_all_regions():
    """ Return a list of all EC2 region names """
    return [r.name for r in boto.ec2.connection.EC2Connection().get_all_regions()]