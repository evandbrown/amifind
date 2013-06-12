import unittest

import amifind

class TestSearch(unittest.TestCase):
    def test_regions(self):
        regions = amifind.search.get_all_regions()
        self.assertEqual(8, len(regions))

    def test_bad_region(self):
        try:
            f = amifind.amifilter.AMIFilter(regions=['middleearth-mordor-1'], owner='amazon')
            images = amifind.search.search_with_filter(f)
        except Exception as ex:
            self.assertEqual(True, isinstance(ex, amifind.exceptions.AMIFilterException), "%s, %s : %s" % (ex.message, type(ex), ex.__class__))

    def test_get_amazon_syd_images(self):
        #f = amifind.amifilter.AMIFilter(regions=['ap-southeast-2'], owner='amazon')
        #result = amifind.search.search_with_filter(f)
        result = amifind.search.search_with_filter(amifind.amifilter.Filters.LINUX_AMAZON_64_PV_EBS.with_region('ap-southeast-2'))
        self.assertNotEqual(0, len(result.regions))
        self.assertNotEqual(0, result.ami_count)

    def test_alinux_uswest2(self):
            result = amifind.search.find_amazon_linux_ebs_64_pv_latest(['us-west-2'])
            self.assertEqual(22, result.ami_count)
if __name__ == '__main__':
    unittest.main()
