import os
import pathlib
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
            print('child full:', os.path.join(cta_root_path, f))
            child = os.path.join(cta_root_path, f)
            if os.path.isdir(child):
                for g in os.listdir(child):
                    grandchild = os.path.join(child, g)
                    print('child child:', g)
                    print('child child full:', grandchild)
                    if os.path.isdir(grandchild):
                        for h in os.listdir(grandchild):
                            ggchild = os.path.join(grandchild, h)
                            print('child child child:', h)
                            print('child child child full:', ggchild)
                    else:
                        print(f'grandchild is not directory: {grandchild}')
            else:
                print(f'child is not directory: {child}')

        full_path = cta_root_path / Path(self.destination_root)
        for f in os.listdir(full_path):
            os.remove(os.path.join(self.destination_root, f))
