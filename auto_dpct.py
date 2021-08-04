import subprocess
import warnings_count
from pathlib import Path

root = Path.cwd()
Path('oneAPI-DirectProgramming-training').mkdir(parents=True, exist_ok=True)
from_dir = root / Path('oneAPI-DirectProgramming')
warning_list = []


def find_cuda_folder():
    subprocess.call('source /opt/intel/oneapi/setvars.sh', shell=True)
    print(Path.cwd())
    for i in from_dir.rglob('*-cuda'):
        project_name = str(i.stem)[:-5]
        # print(str(i.stem))
        Path('oneAPI-DirectProgramming-training/{0}'.format(project_name)).mkdir(parents=True, exist_ok=True)
        generate_dpct(i)


def generate_dpct(path_name):
    cuda_dir = from_dir / Path(path_name)
    project_name = str(path_name.stem)[:-5]
    print(project_name)

    print(Path.cwd())
    for i in cuda_dir.rglob('*.cu'):
        # print(i.parent.name)
        # paths = Path(i.parent.name).joinpath(i.name)
        # print(i.name)

        subprocess.call('dpct --in-root=. {0} --out-root={1}/oneAPI-DirectProgramming-training/{2}/dpcpp/'
                        .format(i.name, root, project_name), shell=True, cwd=i.parent)


def copy_dpct():
    for i in from_dir.rglob('*-dpct'):
        print(str(i))
        project_name = str(i.stem[:-5])
        subprocess.call('cp -rvf {0} {1}/oneAPI-DirectProgramming-training/{2}/dpct-version'
                        .format(i, root, project_name), shell=True)


def count_warnings():
    training_dir = root / Path('oneAPI-DirectProgramming-training')
    dpcpp_dir = training_dir.rglob('*/dpcpp')
    for i in dpcpp_dir:
        for j in i.rglob('*.dp.cpp'):
            print(j)
            sublist = warnings_count.add_to_tuple(str(j))
            if sublist:
                warning_list.extend(sublist)
    print(len(warning_list))
    for k in warning_list:
        print(k)


find_cuda_folder()
copy_dpct()
count_warnings()