from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests

DASHSCOPE_API_KEY = 'sk-2487917f84dd4a948891b51a22a0832e'

app = Flask(__name__)
CORS(app)

@app.route('/')
def root_index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

@app.route('/gpt', methods=['POST'])
def gpt():
    data = request.get_json(force=True)
    prompt = data.get('prompt', '') if data else ''
    if not prompt:
        return jsonify({'error': 'missing prompt'}), 400
    try:
        resp = requests.post(
            'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {DASHSCOPE_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'deepseek-r1',
                'messages': [{ 'role': 'user', 'content': prompt }]
            },
            timeout=30
        )
        return jsonify(resp.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
