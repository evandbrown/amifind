class SearchResult:
    """
    The result of a search executed by amifind.search.search_with_filter(amifind.AMIFilter)
    """
    def __init__(self, result):
        self.result = result
        """ Raw search result """
        
        self.regions = [region for region in result.keys()]
        """ Regions in the search result """
        
        self.all_images = [images for images in result[region] for region in result.keys()]
        """ All images, across all regions, in the result"""
        
        self.ami_count = len(self.all_images)
        """ Total number of images in the search result """
        
        self.one_image_per_region = all(v is True for v in [len(result[region]) == 1 for region in result.keys()])
        """ True if there is exactly one AMI per region """