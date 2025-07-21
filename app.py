from flask import Flask, render_template, request, redirect, url_for, flash, session
from chatbot.chatbot import chatbot_bp
from emergencychatbot.chatbot2 import chatbot2_bp
from locationminiproject.loc import location_bp
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Flask app
app = Flask(__name__, template_folder='website/templates')
app.secret_key = 'your_secret_key'

# Register blueprints
app.register_blueprint(chatbot_bp)
app.register_blueprint(chatbot2_bp, url_prefix='/emergency-response')
app.register_blueprint(location_bp, url_prefix='/location')

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html')

@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('homepage.html')

@app.route('/medication')
def medication():
    return render_template('medication.html')

@app.route('/emergency')
def emergency():
    return render_template('emergency-response-page.html')

@app.route('/consultation')
def consultation():
    return render_template('Medicalconsultation.html')

@app.route('/contact')
def contact():
    return render_template('contact-page.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        blood_group = request.form['blood_group']
        gender = request.form['gender']
        country = request.form['country']
        phone = request.form['phone']

        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        conn.execute('''INSERT INTO users 
                    (first_name, last_name, email, password, blood_group, gender, country, phone) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                    (first_name, last_name, email, hashed_password, blood_group, 
                     gender, country, phone))
        conn.commit()
        conn.close()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('Register.html')

if __name__ == "__main__":
    app.run(debug=True, port=5000)