import streamlit as st
from datetime import datetime
import smtplib

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

# Function to send email
def send_email(to_email, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("your_email@gmail.com", "your_password")  # Replace with your email and password
        server.sendmail("your_email@gmail.com", to_email, content)
        server.quit()
    except Exception as e:
        st.error(f"Error sending email: {str(e)}")

# Home Page
st.title("Live Sessions")
for session_id, session in live_sessions.items():
    st.subheader(session['title'])
    st.write(f"**Topic:** {session['topic']}")
    st.write(f"**Date:** {session['date']} at {session['time']}")
    st.write(f"**Speaker:** {session['speaker']}")
    st.markdown(f"[Join Session]({session['link']})")

# Email Reminder Section
email = st.text_input("Enter your email for reminders:")
if st.button("Set Reminder"):
    if email:
        # Email reminder text
        reminder_text = f"Reminder: {session['title']} by {session['speaker']} on {session['date']} at {session['time']}"
        send_email(email, reminder_text)
        st.success("Reminder set successfully!")
    else:
        st.error("Please enter a valid email.")

# Add to Calendar Section
if st.button("Add to Calendar"):
    session = live_sessions["session_id"]  # Modify if using multiple sessions
    ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
SUMMARY:{session['title']}
DESCRIPTION:{session['topic']}
DTSTART:{datetime.strptime(session['date'], '%Y-%m-%d').strftime('%Y%m%d')}T{session['time'].replace(':', '')}00Z
LOCATION:Online
END:VEVENT
END:VCALENDAR"""
    
    st.download_button("Download Calendar Invite", data=ics_content, file_name=f"{session['title']}.ics", mime='text/calendar')

if __name__ == "__main__":
    st.write("Streamlit app is running.")
