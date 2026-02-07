// Updates the clock every second without asking Python
setInterval(function() {
    const now = new Date();
    const timeString = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const dateString = now.toLocaleDateString([], { weekday: 'long', month: 'long', day: 'numeric' });
    
    const timeElem = document.getElementById('js-clock');
    const dateElem = document.getElementById('js-date');
    
    if(timeElem) timeElem.innerHTML = timeString;
    if(dateElem) dateElem.innerHTML = dateString;
}, 1000);