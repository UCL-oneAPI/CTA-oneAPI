import os
import unittest
from pathlib import Path

from testing_support.BaseTest import BaseTest


class BaseIntegrationTest(BaseTest):
    def setUp(self) -> None:
        full_destination_path = self.cta_root_path / Path(self.destination_root)
        if os.path.exists(full_destination_path):
            self.remove_destination()
        os.mkdir(os.path.join(full_destination_path))

    @property
    def destination_root(self):
        return self.get_full_test_path('integration_testing_data/destination_dir')

    @property
    def dpct_root(self):
        return self.get_full_test_path('integration_testing_data/test_project')

    def tearDown(self) -> None:
        self.remove_destination()

    def remove_destination(self):
        full_destination_path = self.cta_root_path / Path(self.destination_root)
        for f in os.listdir(full_destination_path):
            self.remove_folder(full_destination_path, f)
        os.rmdir(os.path.join(full_destination_path))

    def remove_folder(self, full_path, f_path):
        if os.path.isdir(os.path.join(full_path, f_path)):
            for g in os.listdir(os.path.join(full_path, f_path)):
                self.remove_folder(full_path, os.path.join(f_path, g))
            os.rmdir(os.path.join(full_path, f_path))
        else:
            os.remove(os.path.join(full_path, f_path))
