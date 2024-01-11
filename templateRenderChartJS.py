import json
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
from reportlab.pdfgen import canvas

class ChartJSGraph:
    def __init__(self):
        self.labels = []  # Add labels attribute
        self.datasets = []

    def add_dataset(self, label, data, color=None):
        if color is None:
            # Generate a random color if not provided
            color = f"rgba({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)}, 0.4)"

        dataset = {
            "label": label,
            "data": data,
            "backgroundColor": color,
            "borderColor": color.replace("0.4", "1"),  # Set border color to a fully opaque version of the background color
            "borderWidth": 1,
        }
        self.datasets.append(dataset)

    def to_json(self, x_label, y_label, title):
        chart_data = {
            "type": "line",
            "data": {"labels": self.labels, "datasets": self.datasets},
            "options": {
                "scales": {
                    "y": {"beginAtZero": True},
                    "x": {"title": {"display": True, "text": x_label}},
                },
                "responsive": True,
                "maintainAspectRatio": False,
                "title": {"display": True, "text": title},
                "legend": {"display": True},
            },
        }
        return json.dumps(chart_data)

    def save_plot(self, filename, x_label, y_label, title, page_layout):
        with open(filename + ".html", "w") as html_file:
            html_file.write(self.get_html_template(x_label, y_label, title, page_layout))

        # Read HTML content
        html_content = open(filename + ".html", 'r', encoding='utf-8').read()

        chrome_options = Options()
        chrome_options.add_argument("--headless") 
        chrome_options.add_argument(f"--window-size={816*2},{1056*2}")

        # Create a WebDriver instance using the installed ChromeDriver
        driver = webdriver.Chrome(options=chrome_options)

        try:
            # Open the HTML file in the WebDriver
            driver.get("file://" + 'path_to_the_file'+ filename + ".html")

            # Capture screenshot
            driver.save_screenshot(filename + ".png")

        finally:
            # Close the WebDriver
            driver.quit()
        
        # Open the PNG image
        img = Image.open(filename + ".png")

        # Create a PDF file
        with open(filename + ".pdf", 'wb') as pdf_file:
            # Create a PDF canvas
            pdf_canvas = canvas.Canvas(pdf_file, pagesize=img.size)

            # Draw the PNG image on the PDF canvas
            pdf_canvas.drawInlineImage(filename + ".png", 0, 0, width=img.width, height=img.height)

            # Save the PDF file
            pdf_canvas.save()


    def get_html_template(self, x_label, y_label, title, page_layout):
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Chart.js Example</title>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <style>
                {self.get_layout_style(page_layout)}
            </style>
        </head>
        <body>
            {self.generate_chart_canvas(title, page_layout)}
            <script>
                document.addEventListener('DOMContentLoaded', function() {{
                    {self.generate_chart_scripts(title, page_layout)}
                }});
            </script>
        </body>
        </html>
        """

    def generate_chart_canvas(self, title, page_layout):
        return f"<div id='charts-container'>{self.generate_canvas_elements(title, self.get_num_charts(page_layout))}</div>"

    def generate_canvas_elements(self, title, num_charts):
        return ''.join([f"<div class='chart-container'><canvas id='{title}_{i+1}' width='400' height='400'></canvas></div>" for i in range(num_charts)])

    def generate_chart_scripts(self, title, page_layout):
        scripts = []
        for i in range(1, self.get_num_charts(page_layout) + 1):
            chart_id = f"{title}_{i}"
            scripts.append(f"var ctx{i} = document.getElementById('{chart_id}').getContext('2d');")
            scripts.append(f"var chartData{i} = {self.to_json('X-axis', 'Y-axis', chart_id)};")
            scripts.append(f"var myChart{i} = new Chart(ctx{i}, chartData{i});")
        return '\n'.join(scripts)

    def get_num_charts(self, page_layout):
        if page_layout == "horizontal" or page_layout == "vertical":
            return 4
        elif page_layout == "grid":
            return 6
        else:
            raise ValueError("Invalid page layout")

    def get_layout_style(self, page_layout):
        styles = {
            "horizontal": "#charts-container { display: flex; flex-direction: row; }",
            "vertical": "#charts-container { display: flex; flex-direction: column; }",
            "grid": "#charts-container { display: grid; grid-template-columns: repeat(2, 1fr); grid-gap: 10px; }"
        }
        return styles.get(page_layout, "")


def plot_graph(chart_js_graph, x, y_values, x_label, y_label, title, page_layout):
    chart_js_graph.labels = x
    chart_js_graph.datasets = []

    for i, y in enumerate(y_values):
        chart_js_graph.add_dataset(f"{y_label} {i+1}", y)

    chart_js_graph.save_plot(title, x_label, y_label, title, page_layout)


# Example usage:
x_values = [1, 2, 3, 4, 5]
y_values = [[2, 4, 6, 8, 10], [1, 4, 9, 16, 25]]
x_label = "X-axis"
y_label = "Y-axis"
title = "MyChart.js"

# Create an instance of ChartJSGraph
chart_js_graph = ChartJSGraph()

# Specify the layout
page_layout = "grid"

# Add datasets with specified colors
chart_js_graph.add_dataset("Dataset 1", y_values[0], color="rgba(255, 0, 0, 0.4)")
chart_js_graph.add_dataset("Dataset 2", y_values[1], color="rgba(0, 0, 255, 0.4)")

# Plot the graphs for the specified layout
plot_graph(chart_js_graph, x_values, y_values, x_label, y_label, title, page_layout)

