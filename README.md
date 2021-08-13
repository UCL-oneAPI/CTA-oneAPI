# CTA-oneAPI

This is the main repo for CTA (Code Translation Assistant), a tool that assists developers when completing the semi-automated code migration from CUDA to DPC++ by Intel’s compatibility tool DPCT.  

CTA assists completion:

* Automatically apply fixes  
* Embed recommendations
* Provide report of open warnings & recommendations across code base

Python version: 3.7.9

Website: https://ucl-oneapi.github.io/CTA-oneAPI/

## Installation

### Prerequisites

## Usage
CTA is currently available in two modes.
Use the command below to get the output of default mode (including CTA processed files and a report)  
```Shell
python command_handler.py --mode=default --project-path=auto_editor/sample_data/test_project --destination-path=auto_editor/sample_data/
```
Or set `--mode=read_only` to get report only. 

The `auto_editor/sample_data/test_project` is the path to the DPCT files, and `auto_editor/sample_data/` is the path to the output files.

### For Helps
```Shell
python command_handler.py --help
```

### For Version Information
```Shell
python command_handler.py --version
```