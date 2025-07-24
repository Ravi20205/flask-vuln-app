from flask import Flask, request
import jwt  # known vulnerable versions exist
import yaml  # potential YAML deserialization vulnerability
import requests  # potential SSRF if misused

app = Flask(__name__)

@app.route('/')
def home():
    return 'Welcome to the vulnerable app!'

@app.route('/decode', methods=['POST'])
def decode_token():
    token = request.form['token']
    try:
        # Dangerous: using hardcoded secret and no validation
        decoded = jwt.decode(token, "secret", algorithms=["HS256"])
        return str(decoded)
    except Exception as e:
        return str(e)

@app.route('/load_yaml', methods=['POST'])
def load_yaml():
    content = request.form['yaml']
    # Unsafe: direct loading YAML from untrusted input
    data = yaml.load(content, Loader=yaml.Loader)
    return str(data)

@app.route('/fetch', methods=['GET'])
def fetch():
    url = request.args.get('url')
    r = requests.get(url)  # Potential SSRF vulnerability
    return r.text
