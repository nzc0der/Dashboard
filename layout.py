from dash import dcc, html
import dash_bootstrap_components as dbc

def create_layout(app):
    return html.Div(className='dashboard-container', children=[
        
        # --- Header Section ---
        dbc.Row([
            dbc.Col(html.H1("NEXUS // COMMAND CENTER", className="text-center mb-4"), width=12)
        ]),

        # --- Top Stats Row ---
        dbc.Row([
            # Weather Card
            dbc.Col(html.Div([
                html.H4("Weather Status", className="stat-label"),
                html.Div(id="weather-display", className="stat-value"),
                html.P("Local Conditions", className="text-muted")
            ], className="glass-card"), width=12, md=4),

            # CPU/System Card
            dbc.Col(html.Div([
                html.H4("System Load", className="stat-label"),
                dcc.Interval(id='interval-component', interval=2000, n_intervals=0), # Updates every 2s
                html.Div(id="system-display", className="stat-value"),
                dbc.Progress(id="cpu-progress", value=0, striped=True, animated=True, color="info", className="mt-2", style={"height": "10px"})
            ], className="glass-card"), width=12, md=4),

            # Quote Card
            dbc.Col(html.Div([
                html.H4("Daily Intel", className="stat-label"),
                html.Div(id="quote-display", style={"fontSize": "1.2rem", "fontStyle": "italic", "marginTop": "10px"}),
            ], className="glass-card"), width=12, md=4),
        ], className="mb-4"),

        # --- Main Content Row ---
        dbc.Row([
            # Graph Section
            dbc.Col(html.Div([
                html.H3("Financial Trajectory", className="mb-3"),
                dcc.Graph(id='main-graph', config={'displayModeBar': False})
            ], className="glass-card"), width=12, md=8),

            # Task/List Section
            dbc.Col(html.Div([
                html.H3("Active Protocols", className="mb-3"),
                html.Ul([
                    html.Li("Monitor Server Uptime", className="list-group-item bg-transparent text-white border-0"),
                    html.Li("Review Python Scripts", className="list-group-item bg-transparent text-white border-0"),
                    html.Li("Update API Keys", className="list-group-item bg-transparent text-white border-0"),
                    html.Li("Deploy to Cloud", className="list-group-item bg-transparent text-white border-0"),
                ], className="list-group list-group-flush")
            ], className="glass-card"), width=12, md=4),
        ])
    ])