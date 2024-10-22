from flask import Flask, render_template, redirect, url_for, request
from flask import Flask, render_template, redirect, url_for, request, flash

import re  # Import regex module for password validation
import csv
import os 

app = Flask(__name__)
app.secret_key = '123456789' 

# Route for landing page (index.html)
@app.route('/')
def index():
    return render_template('index.html')

# Function to validate password
def is_valid_password(password):
    # Password must contain at least one uppercase letter, one lowercase letter,
    # one number, one special character, and be at least 8 characters long.
    if (len(password) >= 8 and
        re.search(r"[a-z]", password) and
        re.search(r"[A-Z]", password) and
        re.search(r"[0-9]", password) and
        re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)):
        return True
    return False

# Route for admin login (admin_login.html)
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Check if the email is a valid Gmail address and password is valid
        if email.endswith('@gmail.com') and is_valid_password(password):
            return redirect(url_for('admin_dashboard'))  # Redirect to admin dashboard
        elif email == "admin@example.com" and password == "Admin@123":
            return redirect(url_for('admin_dashboard'))  # Redirect to admin dashboard if admin credentials are correct
        else:
            # If login fails, redirect back to the admin login
            return redirect(url_for('admin_login'))  # Stay on admin login page if invalid credentials
    return render_template('admin_login.html')

# Route for user dashboard
@app.route('/user_dashboard')
def user_dashboard():
    return render_template('user_dashboard.html')

# Route for admin dashboard
@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')

# Route for register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle user registration logic here
        return redirect(url_for('admin_login'))
    return render_template('register.html')

@app.route('/enrollment/<subject>', methods=['GET', 'POST'])
def enrollment(subject):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        date = request.form['date']  # Get the date from the form

        # Save the enrollment data to a CSV file
        csv_file_path = 'static/enrollment_data.csv'
        file_exists = os.path.isfile(csv_file_path)

        # Write to the CSV file
        with open(csv_file_path, mode='a', newline='') as csv_file:
            fieldnames = ['Username', 'Password', 'Subject', 'Date']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()  # Write header only if the file is new

            # Write the enrollment data including the date
            writer.writerow({'Username': username, 'Password': password, 'Subject': subject, 'Date': date})

        flash(f'Enrollment successful for {subject} on {date}!')
        return redirect(url_for('user_dashboard'))

    return render_template('enrollment.html', subject=subject)



@app.route('/attendance', methods=['GET'])
def attendance():
    csv_file_path = 'static/enrollment_data.csv'
    records = []

    # Read the CSV file
    if os.path.isfile(csv_file_path):
        with open(csv_file_path, mode='r') as csv_file:
            reader = csv.DictReader(csv_file)
            records = list(reader)  # Convert to list for easier iteration

    return render_template('attendance.html', records=records)


if __name__ == '__main__':
    app.run(debug=True)
