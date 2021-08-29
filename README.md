

# CTA-oneAPI

This is the main repo for CTA (Code Translation Assistant), a tool that assists developers when completing the semi-automated code migration from CUDA to DPC++ by Intel’s compatibility tool DPCT.  

CTA assists completion:

* Automatically apply fixes  
* Embed recommendations
* Provide report of open warnings & recommendations across code base

Python version: 3.7.9

Website: https://ucl-oneapi.github.io/CTA-oneAPI/

## Installation

### Download
```Shell
git clone https://github.com/UCL-oneAPI/CTA-oneAPI
cd CTA-oneAPI
```

### Prerequisites
Create a virtual environment, e.g. using `venv`.
To install required packages, run `pip install -r -U requirements.txt 
`
Before using the script, you may need to run `export PYTHONPATH=$PYTHONPATH:.` when in the root directory, to avoid import errors

## Usage
CTA is currently available in two modes.
Use the command below to get the output of default mode (including CTA processed files and a report)  
```Shell
python command_handler.py --mode=default --project-path=scripts/sample_data/test_project --destination-path=scripts/sample_data/destination_dir --report-path=scripts/sample_data/report
```
Or set `--mode=read_only` to get report only. 

`auto_editor/sample_data/test_project` is the path to the DPCT files, `auto_editor/sample_data/destination_dir` is the path to the CTA processed files,
and `auto_editor/sample_data/report` is the path to the CTA generated HTML report

## Testing
To run tests, run `python -m unittest`.
To generate a test coverage report, run: 
```Shell
 coverage run -m unittest
 coverage report -m 
```

### For Helps
```Shell
python command_handler.py --help
```

### For Version Information
```Shell
python command_handler.py --version
```

## Report
### Auto-generate Report Example
link:
### Sample Programs Analysis Report
link:
### Special cases Analysis Report
link:
### Warning Message & Suggestion Report
link:
### Analysis Warnings Data
link:
