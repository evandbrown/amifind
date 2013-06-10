import unittest

import amifind

class TestSearch(unittest.TestCase):
    def test_regions(self):
        regions = amifind.search.get_all_regions()
        self.assertEqual(8, len(regions))
    def test_bad_region(self):
        try:
            f = amifind.AMIFilter(regions=['middleearth-mordor-1'], owner='amazon')
            images = amifind.search.search(f)
        except Exception as ex:
            self.assertEqual(True, isinstance(ex, amifind.exceptions.AMIFilterException), "%s, %s : %s" % (ex.message, type(ex), ex.__class__))
    #@unittest.skip
    def test_get_amazon_syd_images(self):
        f = amifind.AMIFilter(regions=['ap-southeast-2'], owner='amazon')
        images = amifind.search.search(f)
        self.assertNotEqual(0, len(images))
if __name__ == '__main__':
    unittest.main()
