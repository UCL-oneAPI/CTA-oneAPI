import os
import unittest


class BaseIntegrationTest(unittest.TestCase):
    @property
    def destination_root(self):
        return 'testing_support/integration_testing_data/destination_dir'

    @property
    def dpct_root(self):
        return 'testing_support/integration_testing_data/test_project'

    def tearDown(self) -> None:
        for f in os.listdir(self.destination_root):
            os.remove(os.path.join(self.destination_root, f))
