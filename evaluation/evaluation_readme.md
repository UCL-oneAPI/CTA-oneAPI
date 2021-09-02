

# Evaluation for CTA-oneAPI

This folder contains the scripting to evaluate the tool.
Specifically, 2 things are done for evaluation:
* evaluate impact on all sample projects of oneAPI-directProgramming repo ()
* evaluate impact on real world repo relevant for the health sector, Relion ()

To run the tool on dpct directprogramming:
* run the mapping tool to add 'dpcpp' subfolders to each project, which contain the dpct warnings
* from the cta base repo, run the evaluation script, e.g.: `python3 evaluation/evaluate_sample_projects.py --projects-root-path="../oneAPI-DirectProgramming-training" --aggregated-report-path="../cta-evaluation-reports"
`