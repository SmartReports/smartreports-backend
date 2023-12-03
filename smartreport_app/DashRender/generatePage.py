from .generatePlot import GeneratePlot
from plotly.subplots import make_subplots

class GeneratePage:
    def __init__(self, page, dir):
        self.page = page
        self.page_layout = self.page.pop('layout')
        self.dir = dir 
        self.fig = make_subplots(rows=self.row_cols()[0], cols=self.row_cols()[1], )
        self.get_charts()
        
    def get_charts(self):
        # self.fig.update_layout(height=1000, width=1000)
        rows = []
        cols = []
        charts = []
        specs = []
        if self.page_layout == 'grid':
            first_type = None
        for i, chart in enumerate(self.page.values()):
            if self.page_layout == 'grid':
                if first_type == None:
                    specs.append([])
                    # specs[i//2].append({'type': self.get_type(chart['chart_type'])})
                    specs[i//2].append(self.get_type(chart['chart_type']))
                    first_type = ''
                else:
                    # specs[i//2].append({'type': self.get_type(chart['chart_type'])})
                    specs[i//2].append(self.get_type(chart['chart_type']))
                    first_type = None
            elif self.page_layout == 'vertical':
                specs.append({'type': self.get_type(chart['chart_type'])})
            elif self.page_layout == 'horizontal':
                specs.append({'type': self.get_type(chart['chart_type'])})
            charts.append(GeneratePlot(chart).fig)
            rows.append(int(i) // self.row_cols()[1] + 1)
            cols.append(int(i) % self.row_cols()[1] + 1)
        if first_type == '':
            tmp = specs[i//2]
            if tmp[0] == {'type': 'polar'}:
                tmp[0] = {'type': 'polar', 'colspan': 2}
            else: tmp[0] = {"colspan": 2}
            specs[i//2] = [tmp[0], None]
        # if self.page_layout == 'horizontal':
            # specs = [specs]
        
        self.fig.update_layout(height=2100, width=2970)
        self.fig.update_layout(showlegend=False)
        self.fig = make_subplots(rows=self.row_cols()[0], cols=self.row_cols()[1],
                                 specs=specs)
        self.fig.add_traces(charts, rows=rows, cols=cols)
            # generate.save_plot(dir=self.dir + '/' + str(i) + '.png')
            
    def row_cols(self):
        if self.page_layout == 'vertical':
            return len(self.page.values()), 1
        elif self.page_layout == 'horizontal':
            return 1, len(self.page.values())
        elif self.page_layout == 'grid':
            rows = len(self.page.values()) // 2
            rows += 1 if len(self.page.values()) % 2 else 0
            return rows, 2
    
    def get_type(self, type):
        if type == 'radar':
            return {'type': 'polar'}
        else:
            return {}