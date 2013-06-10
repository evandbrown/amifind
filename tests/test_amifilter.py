import unittest

import amifind

class TestFilter(unittest.TestCase):
    def test_filter_complete(self):
        f = amifind.AMIFilter(regions=['us-east-1'], owner='amazon')
        self.assertFalse(f.is_complete())
        
        f = amifind.AMIFilter(regions=['us-east-1'], owner='amazon', os='Linux',
                              arch='64', virt_type='pv', root_dev_type='ebs')
        self.assertTrue(f.is_complete())
    def test_ec2_api_filter(self):
        f = amifind.AMIFilter(regions=['us-east-1'], owner='amazon')
        self.assertNotEqual(0, len(f.get_ec2_api_filter()))
        self.assertIsNotNone(f.get_ec2_api_filter())
if __name__ == '__main__':
    unittest.main()
