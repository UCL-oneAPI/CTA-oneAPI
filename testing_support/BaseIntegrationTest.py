import os
import unittest
from pathlib import Path


class BaseIntegrationTest(unittest.TestCase):
    def setUp(self) -> None:
        full_destination_path = self.cta_root_path / Path(self.destination_root)
        if os.path.exists(full_destination_path):
            self.remove_destination()
        os.mkdir(os.path.join(full_destination_path))

    @property
    def cta_root_path(self):
        return Path(__file__).parent.parent.resolve()

    @property
    def destination_root(self):
        return Path.joinpath(self.cta_root_path, 'testing_support', 'integration_testing_data', 'destination_dir')

    @property
    def dpct_root(self):
        return Path.joinpath(self.cta_root_path, 'testing_support', 'integration_testing_data', 'test_project')

    def tearDown(self) -> None:
        self.remove_destination()

    def remove_destination(self):
        full_destination_path = self.cta_root_path / Path(self.destination_root)
        for f in os.listdir(full_destination_path):
            os.remove(os.path.join(full_destination_path, f))
        os.rmdir(os.path.join(full_destination_path))

