from flask import Flask, render_template, request, jsonify, send_file
import os
from dotenv import load_dotenv
from ai_generator import generate_readme
from file_scanner import scan_project
from markdown_export import export_to_markdown
import json

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['GENERATED_FOLDER'] = 'generated'

# Create necessary folders
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['GENERATED_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/scan-project', methods=['POST'])
def scan_project_api():
    """Scan uploaded project and extract structure"""
    try:
        if 'project_file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['project_file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save uploaded file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        # Scan project structure
        project_structure = scan_project(filepath)
        
        return jsonify({
            'success': True,
            'structure': project_structure
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-readme', methods=['POST'])
def generate_readme_api():
    """Generate README using AI"""
    try:
        data = request.json
        
        project_name = data.get('project_name')
        description = data.get('description')
        features = data.get('features', [])
        installation_steps = data.get('installation_steps', [])
        project_structure = data.get('project_structure', '')
        
        if not project_name or not description:
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Generate README using AI
        readme_content = generate_readme(
            project_name=project_name,
            description=description,
            features=features,
            installation_steps=installation_steps,
            project_structure=project_structure
        )
        
        return jsonify({
            'success': True,
            'readme': readme_content
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export-markdown', methods=['POST'])
def export_markdown_api():
    """Export README as markdown file"""
    try:
        data = request.json
        readme_content = data.get('content')
        filename = data.get('filename', 'README')
        
        if not readme_content:
            return jsonify({'error': 'No content provided'}), 400
        
        # Export to markdown
        filepath = export_to_markdown(
            content=readme_content,
            filename=filename,
            output_dir=app.config['GENERATED_FOLDER']
        )
        
        return jsonify({
            'success': True,
            'filepath': filepath,
            'download_url': f'/download/{os.path.basename(filepath)}'
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """Download generated README"""
    try:
        filepath = os.path.join(app.config['GENERATED_FOLDER'], filename)
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)