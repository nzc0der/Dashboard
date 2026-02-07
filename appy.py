import dash
import dash_bootstrap_components as dbc
from layout import create_layout
from callbacks import register_callbacks

# Initialize the app with a dark theme bootstrap
app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.CYBORG],
    title="NEXUS Dashboard"
)

# Set the layout
app.layout = create_layout(app)

# Register interactions
register_callbacks(app)

if __name__ == '__main__':
    # Debug mode is ON so you see errors in the browser
    app.run(debug=True, port=1111)