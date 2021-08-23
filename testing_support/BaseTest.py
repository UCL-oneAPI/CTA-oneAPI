import os
import unittest
from pathlib import Path


class BaseTest(unittest.TestCase):
    @property
    def cta_root_path(self):
        return Path(__file__).parent.parent.resolve()

    def get_full_test_path(self, root: str):
        return Path.joinpath(self.cta_root_path, 'testing_support', root)
