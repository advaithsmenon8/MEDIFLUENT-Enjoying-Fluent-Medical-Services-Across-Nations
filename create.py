import sqlite3

# Connect to the database (replace 'your_database_name.db' with your database file name)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Fetch all records from the users table
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()

# Print each row
print("Data in the 'users' table:")
for row in rows:
    print(row)

# Close the connection
conn.close()



from flask import Blueprint, render_template

app = Flask(__name__)
# Create a Blueprint named 'location'
location_bp = Blueprint('location', __name__, template_folder='templates')

@location_bp.route('/')
def location_page():
    return render_template('index_loc.html')
