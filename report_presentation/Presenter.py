from analysers.PreAnalyser import PreAnalyser
from analysers.PostAnalyser import PostAnalyser
from pathlib import Path
import os
from report_presentation import diff_html, sub_graph, graph_visualization as graph


class Presenter:

    def __init__(self, report_root, dpct_version_root,cta_version_root, initial_warnings, cta_recommendations,final_warnings, changes):

        self.report_root = report_root
        self.initial_warnings = initial_warnings
        self.final_warnings = final_warnings
        self.cta_recommendations = cta_recommendations
        self.changes = changes
        self.dpct_version_root = dpct_version_root
        self.cta_version_root = cta_version_root

    def generate_ui_files(self):
        # Todo: insert code here
        self.run_presenter()

    def html_page(self, all_warnings, recommendations, final_warnings, changes, unique_warning_code, unique_file_path, diff_path):
        file_path_string = self.get_string_of_list(unique_file_path)
        warning_code_string = self.get_string_of_list(unique_warning_code)
        html = self.html_header()
        html += self.basic_analysis(all_warnings, unique_warning_code, unique_file_path, file_path_string, warning_code_string)
        html += self.before_cta_table(all_warnings)
        html += self.after_cta_table(final_warnings)
        html += self.recommendation_table(recommendations)
        warning_fixed = len(all_warnings) - len(final_warnings) - len(recommendations)
        html += self.final_analysis(warning_fixed, recommendations, diff_path)
        html += '''
                <br>
                </body>
                </html>
                '''
        return html

    def get_warning_info(self, warnings):
        html = ""
        num = 0
        for i in warnings:
            num += 1
            message = i.message
            if '<' in message:
                message = message.replace('<', '&lt;')
            if '>' in message:
                message = message.replace('>', '&gt;')
            html += '''
                        <tr>
                                <td class="serif" >%s</td>
                                <td class="serif" >%s</td>
                                <td class="serif" >%s</td>
                                <td class="serif" >%s</td>
                                <td class="serif" >%s</td>
                                <td class="serif" >%s</td>
                        </tr>
                        ''' % (num, i.warning_code, i.file_path, i.project_name, i.line, message)
        return html

    def html_header(self):
        html = '''
                        <html lang="en">
                        <head>
                          <meta charset="UTF-8">
                          <title>CTA Report</title>
                        </head>
                        <h1 align="center">CTA Report</h1>
                        <style> 
                        p.serif{font-family:"Times New Roman",Times,serif;}
                        p.sansserif{font-family:Arial,Helvetica,sans-serif;}
                        body {margin: 50px;}
                        .before-warning-table table, .after-warning-table table, .recommendation-table table, th, td
                          {
                          font-size:0.8em;
                          border:1px solid 	#FFFFFF;
                          padding:10px;
                          }
                         .before-warning-table, .after-warning-table, .recommendation-table
                          {
                          border-collapse:collapse;
                          max-height: 100%;
                          overflow-y: auto;
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
                        <body style="height:100%;"> '''
        return html

    def basic_analysis(self, all_warnings, unique_warning_code, unique_file_path, file_path_string, warning_code_string):
        html_basic_info = '''
                        <p class="serif" ><b>     1.  Number of Analysis Files:  %s</b></p>

                        <p class="serif" ><b>     2.  Analysis Files:    </b></p>
                        <p class="serif" >  %s </p>
                        <p class="serif" ><b>     3.  Number of Warning Type:  %s </b></p>

                        <p class="serif" ><b>     4.  Warning Code Type:    </b></p>
                        <p class="serif" >  %s </p>
                        <p class="serif" ><b>     5.  Total Number of Warnings: %s</b></p>
                        <p class="serif" ><b>     6.  Distribution Graph: </b></p>
                          <img src="images/before-overall.png" width="600" height="450" />
                        <p class="serif" >
                          <a href="subgraphs.html">7.   Sub Graphs for Every File</a>
                        </p>
                        ''' % (len(unique_warning_code), file_path_string, len(unique_file_path), warning_code_string, len(all_warnings))
        return html_basic_info

    def before_cta_table(self, all_warnings):
        html = '''
                        <p class="serif" ><b>     8.  Detailed Warning Information (Before CTA)</b></p>
                        <div class = "before-warning-table">
                        <table border = "0">
                                <tr>
                                        <th>No.</th>
                                        <th>Warning Code</th>
                                        <th>File Path</th>
                                        <th>Project Name</th>
                                        <th>Line Number</th>
                                        <th>Warning message</th>
                                </tr>'''
        html += self.get_warning_info(all_warnings)
        html += '''
                        </table>
                        </div>
                        '''
        return html

    def after_cta_table(self, final_warnings):
        html = '''
                        <p class="serif" ><b>     9.  Detailed Warning Information (After CTA)</b></p>
                        <div class = "after-warning-table">
                        <table border = "0">
                                <tr>
                                        <th>No.</th>
                                        <th>Warning Code</th>
                                        <th>File Path</th>
                                        <th>Project Name</th>
                                        <th>Line Number</th>
                                        <th>Warning message</th>
                                </tr>'''
        html += self.get_warning_info(final_warnings)
        html += '''
                        </table>
                        </div>
                        '''
        return html

    def recommendation_table(self, changes):
        html = '''
                        <p class="serif" ><b>     10.  Detailed Recommendation Information (After CTA)</b></p>
                        <div class = "recommendation-table">
                        <table border = "0">
                                <tr>
                                        <th>No.</th>
                                        <th>Recommendation Code</th>
                                        <th>File Path</th>
                                        <th>Project Name</th>
                                        <th>Line Number</th>
                                        <th>Recommendation message</th>
                                </tr>'''
        html += self.get_recommendation_info(changes)
        html += '''
                        </table>
                        </div>
                        '''
        return html

    def final_analysis(self, warning_fixed, changes, diff_path):
        html = ''
        html += '''
                        <p class="serif" ><b>     11. Number of warnings have been fixed: %s</b></p>
                                ''' % warning_fixed
        html += '''
                        <p class="serif" ><b>     12.  Number of warnings have CTA recommendation: %s</b></p>
                                ''' % len(changes)
        html += '''
                        <p class="serif" ><b>     13.  Comparison of before & after : </b></p>
                        '''
        for file in diff_path.rglob('*.html'):
            html += '''
                    <a href="html_files/%s.html"  class="serif"  >%s</a><br>
                    ''' % (file.stem, file.name)

        return html

    def get_recommendation_info(self, recommendations):
        html = ""
        num = 0
        for i in recommendations:
            num += 1
            message = i.message
            if '<' in message:
                message = message.replace('<', '&lt;')
            if '>' in message:
                message = message.replace('>', '&gt;')
            html += '''
                                <tr>
                                        <td class="serif">%s</td>
                                        <td class="serif">%s</td>
                                        <td class="serif">%s</td>
                                        <td class="serif">%s</td>
                                        <td class="serif">%s</td>
                                        <td class="serif">%s</td>
                                </tr>
                                ''' % (num, i.recommendation_code, i.file_path, i.project_name, i.line, message)
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

    def create_html(self, report_root, dpct_root, destination_root, all_warnings, recommendations, final_warnings, changes, unique_warning_code, unique_file_path):
        diff_path = Path.joinpath(Path(report_root), 'html_files')

        if diff_path.is_dir() and os.listdir(diff_path):
            diff_html.remove_diff_folder(diff_path)
        diff_html.find_dpcpp(dpct_root, destination_root, diff_path)
        for i in os.listdir(report_root):
            join_path = os.path.join(report_root, i)
            if os.path.isfile(join_path):
                os.remove(join_path)
        with open(report_root+'/report.html', 'w') as report:
            report.write(
                self.html_page(all_warnings, recommendations, final_warnings, changes, unique_warning_code, unique_file_path,
                                    diff_path))
        with open(report_root+'/subgraphs.html', 'w') as sub_images:
            sub_images.write(sub_graph.add_images(report_root))

    def remove_image_folder(self, image_path):
        for i in os.listdir(image_path):
            os.remove(os.path.join(image_path, i))
        os.rmdir(image_path)

    def show_visualize(self, report_root, all_warnings):
        image_path = Path.joinpath(Path(report_root), 'images')
        if image_path.is_dir() and os.listdir(image_path):
            Presenter.remove_image_folder(self, image_path)
        image_path.mkdir(parents=True, exist_ok=True)
        graph.visualization_overall(all_warnings, image_path)
        graph.visualization_partial(all_warnings, image_path)

    def get_warnings_and_changes(self, dpct_root, destination_root):
        preAnalyser = PreAnalyser(dpct_root)
        all_warnings = preAnalyser.get_all_warnings()
        postAnalyser = PostAnalyser(destination_root)
        final_warnings = postAnalyser.get_all_warnings()
        changes = postAnalyser.get_all_recommendation()
        return all_warnings, final_warnings, changes

    def run_presenter(self):
        # report_root = Path(__file__).parent
        presenter = Presenter(self.report_root, self.dpct_version_root, self.cta_version_root, self.initial_warnings, self.cta_recommendations, self.final_warnings, self.changes)
        unique_warning_code, unique_file_path = presenter.get_unique_filepath_and_warning_code(self.initial_warnings)

        presenter.show_visualize(self.report_root, self.initial_warnings)
        presenter.create_html(self.report_root, self.dpct_version_root, self.cta_version_root, self.initial_warnings, self.cta_recommendations, self.final_warnings, self.changes, unique_warning_code, unique_file_path)
