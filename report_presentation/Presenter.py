from analysers.PreAnalyser import PreAnalyser
from analysers.PostAnalyser import PostAnalyser
import scripts.run_rule_1003 as run_rule_1003
import sub_graph
from pathlib import Path
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import os


class Presenter:
    def __init__(self, report_root, initial_warnings, final_warnings, changes):
        self.report_root = report_root
        self.initial_warnings = initial_warnings
        self.final_warnings = final_warnings
        self.changes = changes

    def generate_ui_files(self):
        # Todo: insert code here
        pass

    def html_page(self, unique_warning_code, unique_file_path):
        file_path_string = presenter.get_string_of_list(unique_file_path)
        warning_code_string = presenter.get_string_of_list(unique_warning_code)
        html = '''
                <html lang="en">
                <head>
                  <meta charset="UTF-8">
                  <title>CTA Report</title>
                </head>
                <h1 align="center">CTA Report</h1>
                <style> 
                body {margin: 30px;}
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
                <body>
                <p><b>     1.  Number of Analysis Files:  %s</b></p>
                
                <p><b>     2.  Analysis Files:    </b></p>
                <p>  %s </p>
                <p><b>     3.  Number of Warning Type:  %s </b></p>
                 
                <p><b>     4.  Warning Code Type:    </b></p>
                <p>  %s </p>
                <p><b>     5.  Total Number of Warnings: %s</b></p>
                <p><b>     6.  Distribution Graph: </b></p>
                  <img src="images/before-overall.png" width="600" height="450" />
                <p>
                  <a href="subgraphs.html">7.   Sub Graphs for Every File</a>
                </p>
                <p><b>     8.  Detailed Warning Information (Before CTA)</b></p>
                <div class = "before-warning-table">
                <table border = "0">
                        <tr>
                                <th>Warning Code</th>
                                <th>File Path</th>
                                <th>Project Name</th>
                                <th>Line Number</th>
                                <th>Warning message</th>
                        </tr>''' % (len(unique_warning_code), file_path_string, len(unique_file_path), warning_code_string, len(all_warnings))
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
                '''
        html += '''
                <p><b>     9.  Detailed Warning Information (After CTA)</b></p>
                '''
        html += '''
                <p><b>     10.  Detailed Recommendation Information (After CTA)</b></p>
                <div class = "before-warning-table">
                <table border = "0">
                        <tr>
                                <th>Recommendation Code</th>
                                <th>File Path</th>
                                <th>Project Name</th>
                                <th>Line Number</th>
                                <th>Recommendation message</th>
                        </tr>
                </table>
                '''
        html += '''
                <p><b>     11. Number of warnings have been fixed: </b></p>
                        '''
        html += '''
                <p><b>     12.  Number of warnings have CTA recommendation: </b></p>
                        '''
        html += '''
                <p><b>     13.  Comparison of before & after </b></p>
                <p><b>     Diff Link:  </b></p>
                '''
        html += '''
                </div>
                </body>
                </html>
                '''
        return html

    def get_unique_filepath_and_warning_code(self, warnings):
        unique_file_path = []
        unique_warning_code = []
        for i in warnings:
            if i.warning_code not in unique_warning_code:
                unique_warning_code.append(i.warning_code)
            if i.file_path not in unique_file_path:
                unique_file_path.append(i.file_path)
        return unique_warning_code, unique_file_path

    def get_string_of_list(self, alist):
        astring = "    "
        for i in alist:
            astring += i
            astring += " ;   "
        return astring

    def test_get_string_of_list(self, warnings):
        unique_warning_code, unique_file_path = self.get_unique_filepath_and_warning_code(warnings)
        file_path_string = self.get_string_of_list(unique_file_path)
        warning_code_string = self.get_string_of_list(unique_warning_code)
        print(file_path_string)
        print(warning_code_string)

    def visualization_overall(self, warnings, image_path):
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
        plt.yticks(np.arange(0, max(occurrence.values())+1, step=3))
        plt.ylabel("Occurrence")
        plt.title("Warning Types with Number of Occurrences (Overall)")
        plt.legend(loc="upper left", fontsize="x-small")
        plt.savefig(str(image_path) + '/before-overall.png')
        plt.show()

    def visulization_partial(self, warnings, image_path):
        file_warnings = {}
        codes = []
        for i in warnings:
            file_name = Path(i.file_path).name
            file_warnings.setdefault(file_name, []).append(i.warning_code)
            codes.append(i.warning_code)
        codes = set(codes)
        for k, v in file_warnings.items():
            #warning_distribution = {k: Counter(v)}
            warning_distribution = Counter(v)
            for code in codes:
                if code not in warning_distribution.keys():
                    warning_distribution[code] = 0
            x = np.arange(len(codes))
            bar_width = 0.2
            plt.bar(x, warning_distribution.values(), bar_width, align="center", color='blue', alpha=0.5)
            plt.xticks(x, warning_distribution.keys())
            max_value = max(warning_distribution.values()) + 1
            if max_value <= 10:
                step = 1
            else:
                step = 3
            plt.yticks(np.arange(0, max_value, step=step))
            plt.ylabel("Occurrence")
            plt.title("Warnings in " + k)
            plt.savefig(str(image_path) + '/' + k + '.jpg')
            plt.show()

    def remove_image_folder(self, image_path):
        for i in os.listdir(image_path):
            os.remove(os.path.join(image_path, i))
        os.rmdir(image_path)


report_root = Path(__file__).parent
cta_path = Path(__file__).parent.parent.resolve()
dpct_root = Path.joinpath(cta_path, 'testing_support', 'integration_testing_data', 'test_project')
preAnalyser = PreAnalyser(dpct_root)
all_warnings = preAnalyser.get_all_warnings()
postAnalyser = PostAnalyser(dpct_root)
run_rule_1003.call_run_rule()
final_warnings = postAnalyser.get_all_warnings()
print(final_warnings)
changes = []
presenter = Presenter(report_root, all_warnings, final_warnings, changes)
presenter.test_get_string_of_list(all_warnings)
unique_warning_code, unique_file_path = presenter.get_unique_filepath_and_warning_code(all_warnings)

image_path = Path.joinpath(report_root, 'images')
if image_path.is_dir() and os.listdir(image_path):
    presenter.remove_image_folder(image_path)
image_path.mkdir(parents=True, exist_ok=True)
presenter.visualization_overall(all_warnings, image_path)
presenter.visulization_partial(all_warnings, image_path)
with open('test.html', 'w') as report:
    report.write(presenter.html_page(unique_warning_code,unique_file_path))
with open('subgraphs.html', 'w') as sub_images:
    sub_images.write(sub_graph.add_images())
