import os
import unittest
from pathlib import Path


class BaseIntegrationTest(unittest.TestCase):
    @property
    def destination_root(self):
        return 'testing_support/integration_testing_data/destination_dir'

    @property
    def dpct_root(self):
        return 'testing_support/integration_testing_data/test_project'

    def tearDown(self) -> None:
        pre_path = Path.cwd()
        full_path = pre_path / Path(self.destination_root)
        for f in os.listdir(full_path):
            os.remove(os.path.join(self.destination_root, f))
