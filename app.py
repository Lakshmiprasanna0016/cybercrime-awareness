from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from pymongo import MongoClient
import os

app = Flask(__name__)

# Set up template and upload directories
template_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates')
app = Flask(__name__, template_folder=template_dir)

UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set up MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']
collection = db['users']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'GET':
        return "<h2>❗ Please use the form to submit a report.</h2><a href='/'>Go Back</a>"

    try:
        incident_type = request.form.get('type')
        name = request.form.get('name')
        phone = request.form.get('phone')
        description = request.form.get('description')

        file = request.files.get('file')
        filename = None
        if file and file.filename:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

        report = {
            'type': incident_type,
            'name': name,
            'phone': phone,
            'description': description,
            'file': filename
        }

        collection.insert_one(report)

        return render_template('demo.html')


    except Exception as e:
        return f"<h2>❌ ERROR: {e}</h2><a href='/'>Try again</a>"

if __name__ == '__main__':
    app.run(debug=True, threaded=False)
