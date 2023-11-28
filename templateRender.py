import json
from datetime import datetime

import matplotlib.pyplot as plt
import requests
from requests.auth import HTTPBasicAuth
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class TemplateRender:
    def __init__(self,
                 api_base: str = "https://api.smartreports.it/",
                 api_report_endpoint: str = 'report-templates/',
                 api_archive_endpoint: str = '/report-archive/',
                 api_kpis_data_endpoint: str = '/kpi-data/',
                 ):
        self.api_base = api_base
        self.api_report_endpoint = api_report_endpoint
        self.api_archive_endpoint = api_archive_endpoint
        self.api_kpis_data_endpoint = api_kpis_data_endpoint
        self.pages = {}
        self.auth = HTTPBasicAuth('demo', 'Dornys-nunxuq-puxba9')
        self.session = requests.Session()
        self.session.auth = self.auth
        self.session.mount('https://', HTTPAdapter(max_retries=Retry(total=5, backoff_factor=0.1)))
        self.archive = self.request_archive()
        self.reports = self.request_reports()
        self.data = []
        self.request_data_for_report()

    def request_reports(self):
        tmp_reports = self.session.get(self.api_base + self.api_report_endpoint).json()
        for report in tmp_reports:
            if report['id'] in self.archive:
                report['last_sent'] = self.archive[report['id']]['created']
            else:
                report['last_sent'] = ''
        return tmp_reports

    def request_archive(self):
        tmp_archive = self.session.get(self.api_base + self.api_archive_endpoint).json()
        reports_pdf = {}
        # get only the newer one
        for report in tmp_archive:
            if report['template'] not in reports_pdf:
                reports_pdf[report['template']] = report
            elif report['created'] > reports_pdf[report['template']]['created']:
                reports_pdf[report['template']] = report
        return reports_pdf

    def request_data_for_report(self):
        for report in self.reports:
            frequency = self.parse_frequency(report['frequency'])
            if report['last_sent'] != '':
                elapsed = self.to_send(report['last_sent'], frequency)
                if elapsed < frequency:
                    continue
            pages = report['pages']
            report['pages'] = {}
            for page in pages:
                for i, element in enumerate(page['elements']):
                    kpis = ','.join(list([str(kpi) for kpi in element['kpis']]))
                    kpis_data = self.session.get(
                        self.api_base + self.api_kpis_data_endpoint + '/?kpis=' + kpis + '&user_type=' + report[
                            'user_type'] + '&chart_type=' + element['chart_type']).content.decode('utf-8')
                    kpis_data = json.loads(kpis_data)['data']
                    kpis_label = kpis_data['labels']
                    kpis_data = kpis_data['datasets'][0]['data']
                    report['pages'][str(i+1)] = {'data': kpis_data,
                                                 'labels': kpis_label,
                                                 'layout': page['layout'],
                                                 'chart_type': element['chart_type']}
            # report to json
            self.data.append(report)

    def render(self):
        for report in self.data:
            self.plot(report['pages'], report['name'], report)

    def parse_frequency(self, frequency):
        if frequency == "daily":
            return 24
        elif frequency == "weekly":
            return 168
        elif frequency == "monthly":
            return 672
        elif frequency == "quarterly":
            return 2016
        elif frequency == "yearly":
            return 8760
        else:
            raise ValueError("Invalid frequency")

    def to_send(self, date, frequency):
        now = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
        date = datetime.strptime(date.split('.')[0], "%Y-%m-%dT%H:%M:%S")
        elapsed = round((now - date).total_seconds() / 60 / 60) % frequency
        return elapsed

    def plot(self, pages, report_name, data):
        for i, page in enumerate(pages):
            page_layout = page.pop("layout")
            self.plot_graph(range(len(data[page]['data'])), data[page]['data'], 'time', 'value', page_layout,
                            report_name + "page" + str(i))

    def plot_graph(self, x, y, x_label, y_label, page_layout, title):
        page_layout = layout(page_layout, len(x))
        fix, ax = plt.subplots(page_layout[0], page_layout[1])
        ax = ax.flatten()
        for i in range(len(x)):
            ax[i].plot(i, y[i])
            ax[i].set_xlabel(x_label)
            ax[i].set_ylabel(y_label)
            ax[i].set_title(title)
            ax[i].grid()
            ax[i].legend()
            plt.tight_layout()
            plt.savefig(title + ".png")


def layout(page_layout, num_of_charts):
    if page_layout == "horizontal":
        return num_of_charts, 1
    elif page_layout == "vertical":
        return 1, num_of_charts
    elif page_layout == "grid":
        return num_of_charts // 2, 2
    else:
        raise ValueError("Invalid page layout")


archive = [{
    "id": 1,
    "created": "2023-11-27T13:37:23.848243",
    "sent": "false",
    "user_type": "machine_maintainer",
    "file_name":  "DM_Report_Group07.pdf",
    "file": "http://localhost:8000/reports/DM_Report_Group07.pdf",
    "template": 1
}]

data = [{
    "id": 1,
    "pages": [
        {
            "elements": [
                {
                    "id": 2,
                    "kpis": [
                        4,
                        3,
                        5
                    ],
                    "chart_type": "line"
                }
            ],
            "id": 1,
            "layout": "horizontal"
        },
        {
            "elements": [
                {
                    "id": 2,
                    "kpis": [
                        4,
                        5
                    ],
                    "chart_type": "line"
                }
            ],
            "id": 2,
            "layout": "horizontal"
        }
    ],
    "name": "Giacomo",
    "created": "2023-11-24T17:57:44.176959",
    "user_type": "machine_maintainer",
    "frequency": "daily"
}]

template = TemplateRender()
template.render()
