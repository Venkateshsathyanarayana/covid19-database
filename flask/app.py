from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        # Connect to the SQLite database
        conn = sqlite3.connect('vaccine_data.db')
        
        # Get the Aadhaar number entered by the user
        aadhaar_number = int(request.form["aadhaar_number"])
        
        # Search the database for the entered Aadhaar number
        cursor = conn.execute("SELECT * from vaccine_data WHERE Aadhaar_Number = ?", (aadhaar_number,))
        result = cursor.fetchone()
        
        # Check if a record was found for the entered Aadhaar number
        if result is None:
            message = "Sorry, no vaccine record found for the entered Aadhaar number."
        else:
            message = "Vaccine record found for the entered Aadhaar number:"
            message += "<br>Aadhaar Number: " + result[0]
            message += "<br>Name: " + result[1]
            message += "<br>Vaccine: " + result[2]
            message += "<br>Dose: " + str(result[3])
            message += "<br>Date: " + result[4]
            
        
        # Close the database connection
        conn.close()
        
        return message
    
    else:
        return render_template("search.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get the form data submitted by the user
        aadhaar_number = request.form['aadhaar_number']
        name = request.form['name']
        vaccine = request.form['vaccine']
        dose = request.form['dose']
        date = request.form['date']
        
        # Connect to the SQLite database
        
        if len(str(aadhaar_number))==6:
         conn = sqlite3.connect('vaccine_data.db')
        
        # Insert the new record into the database
        conn.execute("INSERT INTO vaccine_data (Aadhaar_Number, Name, Vaccine, Dose, Date) VALUES (?, ?, ?, ?, ?)",
                     (aadhaar_number, name, vaccine, dose, date))
        conn.commit()
        
        # Close the database connection
        conn.close()
        
        # Redirect to the registration success page
        return redirect(url_for('registration_success', aadhaar_number=aadhaar_number))

    else:
        return render_template('register.html')

@app.route('/registration-success/<aadhaar_number>')
def registration_success(aadhaar_number):
    message = "Registration successful for Aadhaar number: " + aadhaar_number
    return render_template('registration_success.html', message=message)


if __name__ == "__main__":
    app.run()