from flask import Flask, render_template, request, jsonify
import time
import os
from detect import load_signatures, load_data, detect_intrusions
from kmp import kmp_search
from naive_search import naive_search

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/signatures', methods=['GET'])
def get_signatures():
    try:
        signatures_file = request.args.get('file', 'signatures.txt')
        signatures = load_signatures(signatures_file)
        return jsonify({
            'success': True,
            'signatures': signatures
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/log', methods=['GET'])
def get_log():
    try:
        log_file = request.args.get('file', 'sample_log.txt')
        with open(log_file, 'r') as f:
            log_content = f.read()
        return jsonify({
            'success': True,
            'content': log_content
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/detect', methods=['POST'])
def detect():
    try:
        data = request.json
        log_content = data.get('log_content')
        signatures = data.get('signatures')
        
        # Write content to temporary files if needed
        if 'log_file' in data:
            log_file = data['log_file']
            with open(log_file, 'r') as f:
                log_content = f.read()
        
        if 'signatures_file' in data:
            signatures_file = data['signatures_file']
            signatures = load_signatures(signatures_file)
        
        # Run KMP detection
        start_time = time.time()
        kmp_results = {}
        for signature in signatures:
            matches = kmp_search(log_content, signature)
            if matches:
                kmp_results[signature] = matches
        kmp_time = time.time() - start_time
        
        # Run Naive detection
        start_time = time.time()
        naive_results = {}
        for signature in signatures:
            matches = naive_search(log_content, signature)
            if matches:
                naive_results[signature] = matches
        naive_time = time.time() - start_time
        
        return jsonify({
            'success': True,
            'kmp_results': kmp_results,
            'kmp_time': kmp_time,
            'naive_results': naive_results,
            'naive_time': naive_time
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

if __name__ == '__main__':
    # Ensure templates and static directories exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000) 