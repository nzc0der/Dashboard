import calendar
from datetime import datetime
from dash import html

def generate_calendar():
    """Generates a responsive HTML grid for the current month."""
    now = datetime.now()
    year, month = now.year, now.month
    
    # FIX: Use TextCalendar or just Calendar to get the matrix
    # monthdayscalendar returns a list of weeks, where each week is a list of days
    cal_obj = calendar.Calendar() 
    month_days = cal_obj.monthdayscalendar(year, month)
    
    month_name = calendar.month_name[month]
    
    # Headers (Mon, Tue, Wed...)
    days_abbr = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    header_row = [html.Div(day, className="cal-day-header") for day in days_abbr]
    
    # Grid Content
    calendar_grid = []
    
    # Add headers first
    calendar_grid.extend(header_row)
    
    # Add days
    for week in month_days:
        for day in week:
            if day == 0:
                calendar_grid.append(html.Div("", className="cal-empty"))
            else:
                is_today = "cal-today" if day == now.day else ""
                calendar_grid.append(html.Div(
                    str(day), 
                    className=f"cal-day {is_today}"
                ))
                
    return html.Div([
        html.H3(f"{month_name} {year}", style={'color': 'white', 'textAlign': 'center'}),
        html.Div(calendar_grid, className="calendar-grid")
    ])

def get_tasks():
    """Simulated Task List"""
    tasks = [
        "Review Monthly Budget",
        "Car Maintenance Appointment",
        "Reply to Client Emails",
        "Gym Session @ 6PM",
        "Read 20 Pages"
    ]
    return [
        html.Div([
            html.Div(className="task-check"),
            html.Span(t, className="task-text")
        ], className="task-item") for t in tasks
    ]