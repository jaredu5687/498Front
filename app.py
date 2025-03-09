from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from agent_two_step import process_code
import feedback as fb  # Added import for feedback handling

app = Flask(__name__, template_folder='templates')
CORS(app)  # This allows frontend to make requests to this backend

@app.route('/')
def index():
    return render_template('index.html')  # This renders the HTML file

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



        feedback_text = request.form.get('feedback', '').strip()  # Get feedback from text box
        if feedback_text:
            fb.init_feedback_log()
            new_feedback = fb.process_feedback(feedback_text)
            fb.save_feedback(new_feedback)


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
        model = Ollama(model='codellama:7b')
    except Exception as e:
        print(f"Failed to connect to Ollama: {str(e)}")
    
    app.run(host='0.0.0.0', debug=True, port=5006)