
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import smtplib

app = Flask(_name_)

# Sample data for live sessions
live_sessions = {
    "session_id": {
        "title": "Live Session with Professor X",
        "topic": "Future Trends in Management Education",
        "date": "2023-10-20",
        "time": "18:00",
        "speaker": "Professor Y",
        "link": "http://live-session-link.com"
    }
}

@app.route('/')
def home():
    return render_template('announcement.html', live_sessions=live_sessions)

@app.route('/join_session/<session_id>')
def join_session(session_id):
    session = live_sessions.get(session_id)
    if session:
        return redirect(session['link'])
    return "Session not found", 404

@app.route('/set_reminder/<session_id>', methods=["POST"])
def set_reminder(session_id):
    email = request.form['email']
    session = live_sessions.get(session_id)
    if session:
        # Simplified email sending logic
        reminder_text = f"Reminder: {session['title']} by {session['speaker']} on {session['date']} at {session['time']}"
        send_email(email, reminder_text)
        return "Reminder set successfully"
    return "Session not found", 404

@app.route('/add_to_calendar/<session_id>')
def add_to_calendar(session_id):
    session = live_sessions.get(session_id)
    if session:
        # Add to calendar logic, generate ICS file for download
        ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
SUMMARY:{session['title']}
DESCRIPTION:{session['topic']}
DTSTART:{datetime.strptime(session['date'], '%Y-%m-%d').strftime('%Y%m%d')}T{session['time'].replace(':', '')}00Z
LOCATION:Online
END:VEVENT
END:VCALENDAR"""
        return ics_content, 200, {
            'Content-Type': 'text/calendar',
            'Content-Disposition': f'attachment; filename={session["title"]}.ics'
        }
    return "Session not found", 404

def send_email(to_email, content):
    # Simplified example, replace with your SMTP server credentials
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("your_email@gmail.com", "password")
        server.sendmail("your_email@gmail.com", to_email, content)
        server.quit()
    except Exception as e:
        print(f"Error: {str(e)}")

if _name_ == '_main_':
    app.run(debug=True)
