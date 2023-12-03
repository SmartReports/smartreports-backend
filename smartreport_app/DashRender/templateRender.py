import json
from datetime import datetime
from typing import Any
import requests
from requests.auth import HTTPBasicAuth
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from .generateReport import GenerateReport
import base64
from pathlib import Path

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
        self.gen()

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
            for j, page in enumerate(pages):
                for i, element in enumerate(page['elements']):
                    kpis = ','.join(list([str(kpi) for kpi in element['kpis']]))
                    kpis_data = self.session.get(
                        self.api_base + self.api_kpis_data_endpoint + '/?kpis=' + kpis + '&user_type=' + report[
                            'user_type'] + '&chart_type=' + element['chart_type']).content.decode('utf-8')
                    kpis_data = json.loads(kpis_data)['data']
                    kpis_label = kpis_data['labels']
                    kpis_data = kpis_data['datasets'][0]['data']
                    if str(j) not in report['pages']:
                        report['pages'][str(j)] = {'layout': page['layout']}
                    report['pages'][str(j)][str(i+1)] = {'data': kpis_data,
                                                 'labels': kpis_label,
                                                 'chart_type': element['chart_type']}
            # report to json
            self.data.append(report)

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
    
    def gen(self) -> Any:
        self.new_archive = {}
        for report in self.data:
            name = str(report['id']) + '_' + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if report["user_type"] not in self.new_archive:
                self.new_archive[report["user_type"]] = {}
            self.new_archive[report["user_type"]][report['id']] = {'file': GenerateReport(report, dir=f'DashRender/reports/{report["user_type"]}/').generate(name=name), 'file_name': report["name"] + '_' + name + '.pdf'}
            print(f'Report {report["name"]} generated successfully')
            
        output=  {}
        for user in self.new_archive:
            for report in self.new_archive[user]:
                if user not in output:
                    output[user] = {}
                if report not in output[user]:
                    output[user][report] = {}
                output[user][report] = {"file": self.pdf_to_base64(self.new_archive[user][report]['file']), "file_name": self.new_archive[user][report]['file_name']}

        output2 = []
        for user in output:
            for report in output[user]:
                output2.append({
                    "user_type": user,
                    "template": report,
                    "file": output[user][report]['file'],
                    "file_name": output[user][report]['file_name']
                })
        for elem in output2:
            self.session.post(self.api_base + self.api_archive_endpoint, json=elem)
            
    
    def pdf_to_base64(self, pdf_path):
        with open(pdf_path, 'rb') as f:
            pdf_data = f.read()
        pdf_to_base64 = 'data:application/pdf;base64,' + base64.b64encode(pdf_data).decode('utf-8')
        Path(pdf_path).unlink()
        return pdf_to_base64


TemplateRender()
