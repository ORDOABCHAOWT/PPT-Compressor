from flask import Flask, render_template, request, send_file, jsonify
import os
from werkzeug.utils import secure_filename
from ppt_compressor_v3 import ModernPPTCompressor
import shutil
from pathlib import Path
import time

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['COMPRESSED_FOLDER'] = 'compressed'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB limit

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['COMPRESSED_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compress', methods=['POST'])
def compress_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and (file.filename.endswith('.ppt') or file.filename.endswith('.pptx')):
        filename = secure_filename(file.filename)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(upload_path)
        
        preset = request.form.get('preset', 'balanced')
        
        try:
            # Initialize compressor
            compressor = ModernPPTCompressor(preset=preset)
            
            # Define output path
            output_filename = f"compressed_{filename}"
            output_path = os.path.join(app.config['COMPRESSED_FOLDER'], output_filename)
            
            # Compress
            compressor.compress_ppt(upload_path, output_path)
            
            # Get stats
            original_size = os.path.getsize(upload_path)
            compressed_size = os.path.getsize(output_path)
            reduction = original_size - compressed_size
            percent = (reduction / original_size) * 100
            
            return jsonify({
                'success': True,
                'filename': output_filename,
                'original_size': compressor.format_size(original_size),
                'compressed_size': compressor.format_size(compressed_size),
                'reduction': f"{percent:.1f}%",
                'download_url': f"/download/{output_filename}"
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            # Cleanup upload
            if os.path.exists(upload_path):
                os.remove(upload_path)
                
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['COMPRESSED_FOLDER'], filename), as_attachment=True)

def cleanup_old_files():
    """Cleanup files older than 1 hour"""
    now = time.time()
    for folder in [app.config['UPLOAD_FOLDER'], app.config['COMPRESSED_FOLDER']]:
        for f in os.listdir(folder):
            f_path = os.path.join(folder, f)
            if os.stat(f_path).st_mtime < now - 3600:
                os.remove(f_path)

if __name__ == '__main__':
    # Cleanup on start
    if os.path.exists(app.config['UPLOAD_FOLDER']):
        shutil.rmtree(app.config['UPLOAD_FOLDER'])
    if os.path.exists(app.config['COMPRESSED_FOLDER']):
        shutil.rmtree(app.config['COMPRESSED_FOLDER'])
        
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['COMPRESSED_FOLDER'], exist_ok=True)
    
    app.run(debug=True, port=5001)
