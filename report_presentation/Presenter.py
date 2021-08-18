from analysers.PreAnalyser import PreAnalyser
from pathlib import Path
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt


class Presenter:
    def __init__(self, report_root, initial_warnings, final_warnings, changes):
        self.report_root = report_root
        self.initial_warnings = initial_warnings
        self.final_warnings = final_warnings
        self.changes = changes

    def generate_ui_files(self):
        # Todo: insert code here
        pass

    def html_page(self):
        # cta_path = Path(__file__).parent.parent.resolve()
        # dpct_root = Path.joinpath(cta_path, 'testing_support', 'integration_testing_data', 'test_project')
        # preAnalyser = PreAnalyser(dpct_root)
        # all_warnings = PreAnalyser.get_all_warnings(preAnalyser)
        html = '''
                <html lang="en">
                <head>
                  <meta charset="UTF-8">
                  <title>CTA Report</title>
                </head>
                <h1 align="center">CTA Report</h1>
                <style> 
                .before-warning-table table,th, td
                  {
                  font-size:0.8em;
                  border:1px solid 	#FFFFFF;
                  padding:5px;
                  }
                  table
                  {
                  border-collapse:collapse;
                  }
                th
                  {
                  font-size:1em;
                  text-align:left;
                  padding-top:5px;
                  padding-bottom:4px;
                  background-color:	#4169E1;
                  color:#ffffff;
                  }
                tr:nth-child(even)
                  {background-color: #F2F2F2;}
                
                </style>
                <body><ul>
                <li>Total Number of Warnings: %s</li>
                <p>
                  <img src="before-histogram.jpg" width="400" height="300" />
                </p>
                <li>Detailed Warning Information</li>
                <div class = "before-warning-table">
                <table border = "0">
                        <tr>
                                <th>Warning Code</th>
                                <th>File Path</th>
                                <th>Project Name</th>
                                <th>Line Number</th>
                                <th>Warning message</th>
                        </tr>''' % (len(all_warnings))
        for i in all_warnings:
            message = i.message
            if '<' in message:
                message = message.replace('<', '&lt;')
            if '>' in message:
                message = message.replace('>', '&gt;')
            html += '''
                        <tr>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                        </tr>
                        ''' % (i.warning_code, i.file_path, i.project_name, i.line, message)

        html += '''
                </table>
                </div>
                </ul>
                </body>
                </html>
                '''
        return html


def visualization(warnings):
    warning_codes = []
    file_codes = {}
    files_contain_warnings = {}
    for i in warnings:
        warning_codes.append(i.warning_code)
        file_codes.setdefault(i.warning_code, []).append(i.file_path)
    occurrence = Counter(warning_codes)
    print(occurrence)

    for k, v in file_codes.items():
        files_contain_warnings[k] = len(list(set(v)))

    x = np.arange(len(occurrence.keys()))
    bar_width = 0.2
    plt.figure(2)
    #plt.bar(occurrence.keys(), occurrence.values(), 0.2, color='blue', alpha=0.8)
    plt.bar(x, occurrence.values(), bar_width, align="center", color="green", label="Number of Occurrences", alpha=0.5)
    plt.bar(x + bar_width, files_contain_warnings.values(), bar_width, align="center", color="blue", label="Number of documents containing such warnings",
            alpha=0.5)
    plt.xticks(x + bar_width / 2, occurrence.keys())
    #plt.xlabel("X-axis")
    plt.ylabel("Occurrence")
    plt.yticks(np.arange(0, max(occurrence.values())+1, step=3))
    #plt.title("Warning Types with Number of Occurrences")
    plt.legend(loc="upper left", fontsize="x-small")
    plt.savefig('before-histogram.jpg')
    plt.show()



report_root = Path(__file__).parent
cta_path = Path(__file__).parent.parent.resolve()
dpct_root = Path.joinpath(cta_path, 'testing_support', 'integration_testing_data', 'test_project')
preAnalyser = PreAnalyser(dpct_root)
all_warnings = PreAnalyser.get_all_warnings(preAnalyser)
final_warnings = []
changes = []
presenter = Presenter(report_root, all_warnings, final_warnings, changes)
visualization(all_warnings)
with open('test.html', 'w') as f:
    f.write(presenter.html_page())
