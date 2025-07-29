from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)   # ✅ Define app first
CORS(app)

# Validation function
def is_valid_url(url):
    pattern = re.compile(
        r'^(https?:\/\/)?'
        r'(([a-zA-Z0-9\-]+\.)+[a-zA-Z]{2,})'
        r'(\/[a-zA-Z0-9@:%_\+.~#?&//=]*)?$',
        re.IGNORECASE
    )
    if not re.match(pattern, url):
        return False
    return True

# API route
@app.route('/check_url', methods=['POST'])
def check_url():
    data = request.get_json()
    url = data.get('url', '')
    valid = is_valid_url(url)
    return jsonify({
        'valid': valid,
        'message': '✅ Valid URL' if valid else '❌ Invalid URL'
    })

if __name__ == '__main__':
    app.run(debug=True)
