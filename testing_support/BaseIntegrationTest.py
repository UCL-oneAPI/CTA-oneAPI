import os
import unittest
from pathlib import Path


class BaseIntegrationTest(unittest.TestCase):
    @property
    def destination_root(self):
        return Path.joinpath(Path('testing_support'), 'integration_testing_data', 'destination_dir')

    @property
    def dpct_root(self):
        return Path.joinpath(Path('testing_support'), 'integration_testing_data', 'test_project')

    def tearDown(self) -> None:
        cta_root_path = Path(__file__).parent.parent.resolve()
        print('at teardown:', cta_root_path)

        for f in os.listdir(cta_root_path):
            print('child:', f)
            print('full:', os.path.join(self.destination_root, f))

        full_path = cta_root_path / Path(self.destination_root)
        for f in os.listdir(full_path):
            os.remove(os.path.join(self.destination_root, f))
