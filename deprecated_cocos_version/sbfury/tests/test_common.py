import unittest
import sys
sys.path.append('./')
from test import *

import common

class TestCommon(unittest.TestCase):

    def test_load_image(self):
        common.load_image('dragon/head.png')
        common.load_image('dragon/part.png')

if __name__ == '__main__':
    unittest.main()
