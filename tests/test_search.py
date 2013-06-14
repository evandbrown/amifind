import unittest

from amifind import amifind
from amifind import amifilter

class TestSearch(unittest.TestCase):
    def test_regions(self):
        regions = amifind.get_all_regions()
        self.assertEqual(8, len(regions))

    def test_bad_region(self):
        try:
            f = amifilter.AMIFilter(regions=['middleearth-mordor-1'], owner='amazon')
            images = amifind.find(f)
        except Exception as ex:
            self.assertEqual(True, isinstance(ex, amifind.exceptions.AMIFilterException), "%s, %s : %s" % (ex.message, type(ex), ex.__class__))

    def test_get_amazon_syd_images(self):
        result = amifind.find(amifind.Filters.LINUX_AMAZON_64_PV_EBS.with_regions(['ap-southeast-2']))
        self.assertEqual(1, len(result.regions))
        self.assertNotEqual(0, result.ami_count)

    def test_alinux_uswest2(self):
        result = amifind.amazon_linux_ebs_64_pv(['us-west-2'])
        self.assertEqual(13, result.ami_count)

    def test_alinux_apnortheast1_latest(self):
        result = amifind.amazon_linux_ebs_64_pv_latest(['ap-northeast-1'])
        self.assertEqual(1, result.ami_count)
    @unittest.skip        
    def test_alinux_latest_everywhere(self):
        result = amifind.amazon_linux_ebs_64_pv_latest()
        self.assertEqual(True, result.one_image_per_region)
        
if __name__ == '__main__':
    unittest.main()
