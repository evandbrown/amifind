import unittest

import amifind

class TestSearch(unittest.TestCase):
    def test_regions(self):
        regions = amifind.search.get_all_regions()
        self.assertEqual(8, len(regions))        
        
if __name__ == '__main__':
    unittest.main()
