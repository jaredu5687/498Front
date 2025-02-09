from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from agent_two_step import process_code

app = Flask(__name__)
CORS(app)  # This allows frontend to make requests to this backend

@app.route('/api/analyze', methods=['POST'])
def analyze_code():
    try:
        if 'codeFile' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['codeFile']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Read the contents of the file
        code_content = file.read().decode('utf-8')
        
        # Process the code using your AI agents
        result = process_code(code_content)
        
        return jsonify({'result': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 