import dash
from layout import create_layout

# Initialize the app
app = dash.Dash(__name__, title="LifeHUD")

# Set the layout
app.layout = create_layout()

if __name__ == '__main__':
    # Standard run - go to http://127.0.0.1:8050/
    app.run(debug=True, port=8050)