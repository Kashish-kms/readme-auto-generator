import os
import sys
from flask import Flask, render_template, request, jsonify, send_file
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__, 
            template_folder='../templates', 
            static_folder='../static',
            static_url_path='/static')

# Configuration
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
app.config['GENERATED_FOLDER'] = '/tmp/generated'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create necessary folders
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['GENERATED_FOLDER'], exist_ok=True)

# Import after Flask app creation
try:
    from ai_generator import generate_readme
    from file_scanner import scan_project
    from markdown_export import export_to_markdown
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(1)

# Routes
@app.route('/')
def index():
    """Home page"""
    try:
        return render_template('index.html')
    except Exception as e:
        return jsonify({'error': f'Template error: {str(e)}'}), 500

@app.route('/dashboard')
def dashboard():
    """Dashboard page"""
    try:
        return render_template('dashboard.html')
    except Exception as e:
        return jsonify({'error': f'Template error: {str(e)}'}), 500

@app.route('/api/generate-readme', methods=['POST'])
def generate_readme_api():
    """Generate README using AI"""
    try:
        data = request.json
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        project_name = data.get('project_name', '').strip()
        description = data.get('description', '').strip()
        features = data.get('features', [])
        installation_steps = data.get('installation_steps', [])
        project_structure = data.get('project_structure', '')
        
        # Validate required fields
        if not project_name or not description:
            return jsonify({'error': 'Project name and description are required'}), 400
        
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
        print(f"Error in generate_readme_api: {str(e)}")
        return jsonify({'error': f'Generation error: {str(e)}'}), 500

@app.route('/api/export-markdown', methods=['POST'])
def export_markdown_api():
    """Export README as markdown file"""
    try:
        data = request.json
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        readme_content = data.get('content', '').strip()
        filename = data.get('filename', 'README').strip()
        
        if not readme_content:
            return jsonify({'error': 'No content provided'}), 400
        
        # Sanitize filename
        filename = ''.join(c for c in filename if c.isalnum() or c in (' ', '-', '_')).strip()
        if not filename:
            filename = 'README'
        
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
        print(f"Error in export_markdown_api: {str(e)}")
        return jsonify({'error': f'Export error: {str(e)}'}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """Download generated README"""
    try:
        # Prevent directory traversal
        filename = os.path.basename(filename)
        filepath = os.path.join(app.config['GENERATED_FOLDER'], filename)
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(filepath, as_attachment=True, download_name=filename)
    except Exception as e:
        print(f"Error in download_file: {str(e)}")
        return jsonify({'error': f'Download error: {str(e)}'}), 500

# Error Handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Page not found'}), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

# Health check endpoint
@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'}), 200

# For local development
if __name__ == '__main__':
    app.run(debug=True, port=5000)
