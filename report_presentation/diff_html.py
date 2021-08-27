import difflib
from pathlib import Path
import os


def find_dpcpp(dpct_root, destination_root, diff_path):
    for i in dpct_root.rglob('*.dp.cpp'):
        dpcpp_path = str(i.parent)
        dpct_file_name = i.stem[:-3]
        for j in destination_root.rglob('*.dp.cpp'):
            cta_file_name = j.stem[:-3]
            if dpct_file_name == cta_file_name:
                dpct_path = str(j.parent)
                generate_html(diff_path, dpcpp_path+'/'+dpct_file_name+'.dp.cpp', dpct_path+'/'+dpct_file_name+'.dp.cpp', dpct_file_name)


def generate_html(diff_path, file1, file2, name):
    read1 = read_file(file1)
    read2 = read_file(file2)
    html_diff = difflib.HtmlDiff()
    with open(name+'.html', 'a+') as output:
        output.write(html_diff.make_file(read1, read2))
        output.close()
    diff_path.mkdir(parents=True, exist_ok=True)
    html_path = Path.joinpath(diff_path, name+'.html')
    Path(name+'.html').rename(html_path)


def read_file(file):
    f = open(file, "r+", encoding='UTF-8')
    read = f.readlines()
    return read


def remove_diff_folder(diff_path):
    for i in os.listdir(diff_path):
        os.remove(os.path.join(diff_path, i))
    os.rmdir(diff_path)
