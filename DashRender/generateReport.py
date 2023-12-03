import json
from generatePage import GeneratePage
from pprint import pprint
from pathlib import Path
from PIL import Image
__all__ = ['GenerateReport']

class GenerateReport:
    def __init__(self, report: json, dir) -> None:
        self.report = report
        self.dir = dir + '/' + self.report['name'] 
        self.path = Path(self.dir)
        self.path.mkdir(parents=True, exist_ok=True)
        self.pages = []
                
    def generate(self, name):
        for i, page in enumerate(self.report['pages'].values()):
            page = GeneratePage(page, self.dir)
            page.fig.write_image(self.dir + '/page_' + str(i) + '.png')
            self.pages.append(self.dir + '/page_' + str(i) + '.png')
            
        first_page_path = self.pages.pop(0)
        first_page = Image.open(first_page_path)
        first_page = first_page.convert('RGB')
        pages = [Image.open(page) for page in self.pages]
        pages = [page.convert('RGB') for page in pages]
        first_page.save(self.dir + '_' + name + '.pdf', save_all=True, append_images=pages)
        # delete pngs
        for page in self.pages:
            Path(page).unlink()
        Path(first_page_path).unlink()
        Path(self.dir + '/').rmdir()
            
        # print(f'Report {self.report["name"]} generated successfully')
        return self.dir + '_' + name + '.pdf'