from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
__all__ = ["GeneratePlot"]

class GeneratePlot:
    def __init__(self, data) -> None:
        self.chart_type = data.pop("chart_type")
        self.data = data
        self.fig = self.select_chart(self.chart_type)

    def select_chart(self, chart_type: str):
        if chart_type == "bar":
            return go.Bar(x=self.data['labels'], y=self.data['data'])
        elif chart_type == "line":
            return go.Line(x=self.data['labels'], y=self.data['data'])
        elif chart_type == "radar":
            return go.Scatterpolar(r=self.data['data'], theta=self.data['labels'])
        elif chart_type == "pie" or chart_type == "doughnut":
            return go.Pie(values=self.data['data'], names=self.data['labels'])
        else:
            return None
        
    def save_plot(self, dir):
        self.fig.write_image(dir)
        
    def get_plot(self):
        return self.fig