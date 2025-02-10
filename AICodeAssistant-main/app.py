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

        try:
            code_content = file.read().decode('utf-8')
        except Exception as e:
            return jsonify({'error': 'Error reading file content'}), 400

        try:
            result = process_code(code_content)
            return jsonify({'result': result})
        except Exception as e:
            return jsonify({'error': f'AI processing error: {str(e)}'}), 500

    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    try:
        from langchain_community.llms import Ollama
        model = Ollama(model="codellama:7b")
    except Exception as e:
        print(f"Failed to connect to Ollama: {str(e)}")
    
    app.run(host='0.0.0.0', debug=False, port=5001) 