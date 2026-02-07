from dash.dependencies import Input, Output
import plotly.graph_objects as go
from data_manager import DataManager

data_mgr = DataManager()

def register_callbacks(app):
    
    # Callback to update weather, quotes, and system stats
    @app.callback(
        [Output("weather-display", "children"),
         Output("system-display", "children"),
         Output("cpu-progress", "value"),
         Output("quote-display", "children")],
        [Input("interval-component", "n_intervals")]
    )
    def update_metrics(n):
        # Fetch data
        weather = data_mgr.get_weather()
        sys_status = data_mgr.get_system_status()
        quote = data_mgr.get_quote() if n == 0 else dash.no_update # Only fetch quote once on load
        
        # Format Weather
        weather_text = f"{weather['temperature']}°C"
        
        # Format System
        cpu_text = f"CPU: {sys_status['cpu']}%"
        
        return weather_text, cpu_text, sys_status['cpu'], quote

    # Callback to update graph
    @app.callback(
        Output("main-graph", "figure"),
        [Input("interval-component", "n_intervals")]
    )
    def update_graph(n):
        # Create a cool dark-mode graph
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=data_mgr.crypto_data['Dates'], 
            y=data_mgr.crypto_data['Bitcoin'],
            mode='lines',
            name='BTC',
            line=dict(color='#38bdf8', width=3),
            fill='tozeroy',
            fillcolor='rgba(56, 189, 248, 0.1)'
        ))

        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#94a3b8'),
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
        )
        return fig
    
    # Need to import dash here for no_update check or pass it in
    import dash