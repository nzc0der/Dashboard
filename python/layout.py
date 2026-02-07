from dash import html, dcc
import widgets

def create_layout():
    return html.Div(className='hud-container', children=[
        
        # 1. Clock Widget (Top Left)
        html.Div(className='hud-card area-clock', children=[
            html.Div(id='js-clock', className='time-display', children="00:00"),
            html.Div(id='js-date', className='date-display', children="Loading Date...")
        ]),

        # 2. Header / Weather (Top Middle/Right)
        html.Div(className='hud-card area-header', children=[
            html.H1("PERSONAL COMMAND // HOMEBASE", style={'margin': 0, 'fontSize': '1.5rem', 'letterSpacing': '3px'})
        ]),

        # 3. Sidebar (Left) - Quick Links / Status
        html.Div(className='hud-card area-sidebar', children=[
            html.H2("System Status"),
            html.P("Internet: Connected (1Gbps)", className="text-muted"),
            html.P("VPN: Active - Tokyo", className="text-muted"),
            html.Hr(style={'borderColor': 'rgba(255,255,255,0.1)'}),
            html.H2("Quick Links"),
            html.Ul([
                html.Li("Spotify Control"),
                html.Li("Smart Home Hub"),
                html.Li("Server Logs")
            ], style={'listStyle': 'none', 'padding': 0, 'lineHeight': '2'})
        ]),

        # 4. Main Calendar (Center)
        html.Div(className='hud-card area-main', children=[
            widgets.generate_calendar()
        ]),

        # 5. Todo List (Right)
        html.Div(className='hud-card area-notes', children=[
            html.H2("Priority Tasks"),
            html.Div(widgets.get_tasks(), style={'overflowY': 'auto'})
        ]),

        # 6. Footer / News Ticker (Bottom)
        html.Div(className='hud-card area-footer', children=[
            html.H2("Notes & Reminders"),
            html.Textarea(
                placeholder="Type quick notes here...",
                style={
                    'width': '100%', 
                    'height': '100%', 
                    'background': 'transparent', 
                    'border': 'none', 
                    'color': 'white', 
                    'resize': 'none',
                    'fontFamily': 'JetBrains Mono'
                }
            )
        ]),
    ])