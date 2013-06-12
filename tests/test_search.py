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
            images = amifind.with_filter(f)
        except Exception as ex:
            self.assertEqual(True, isinstance(ex, amifind.exceptions.AMIFilterException), "%s, %s : %s" % (ex.message, type(ex), ex.__class__))

    def test_get_amazon_syd_images(self):
        result = amifind.with_filter(amifind.amifilter.Filters.LINUX_AMAZON_64_PV_EBS.with_regions(['ap-southeast-2'], replace=True))
        self.assertEqual(1, len(result.regions))
        self.assertNotEqual(0, result.ami_count)

    def test_alinux_uswest2(self):
            result = amifind.amazon_linux_ebs_64_pv_latest(['us-west-2'])
            self.assertEqual(22, result.ami_count)
if __name__ == '__main__':
    unittest.main()
