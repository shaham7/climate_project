import dash
from dash import dcc, html
import plotly.express as px

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Test Dash App"),
    dcc.Graph(
        figure=px.line(x=[1, 2, 3], y=[4, 5, 6], title="Simple Line Plot")
    )
])

if __name__ == '__main__':
    import sys
    
    if sys.platform == 'darwin':  # Check if running on macOS
        app.run_server(
            host='127.0.0.1',
            port=8050,
            debug=False  # Set debug to False for testing
        )
    else:
        app.run_server(debug=True)