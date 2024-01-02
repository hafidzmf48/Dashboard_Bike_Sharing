import streamlit as st
import sqlite3
import csv
from io import StringIO

# Define your secret key or password
SECRET_KEY = "your_secret_password"

# Create a connection to SQLite database
conn = sqlite3.connect('feedback.db')
c = conn.cursor()

# ... (Existing code to create table, get user feedback, and store feedback)

# Function to download feedback as a CSV file
def download_feedback_as_csv(data):
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Feedback'])  # Write header
    writer.writerows(data)
    output.seek(0)
    return output.getvalue().encode('utf-8')

# Display the stored feedback from the database
st.header("Stored Feedback")
c.execute("SELECT user_feedback FROM feedback")
stored_feedback = c.fetchall()
for feedback in stored_feedback:
    st.write(feedback[0])

# Access control for download button
password_input = st.text_input("Enter password to download feedback as CSV:")
if password_input == SECRET_KEY:
    if st.button('Download Feedback as CSV'):
        feedback_data = [feedback[0] for feedback in stored_feedback]
        csv_feedback = download_feedback_as_csv(feedback_data)
        st.download_button(
            label="Click here to download",
            data=csv_feedback,
            file_name="feedback_data.csv",
            mime="text/csv"
        )

# Close the connection
conn.close()
