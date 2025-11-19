from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
import time
import random

app = Flask(__name__)
app.secret_key = '6524c3b8008c1029d49c5f32d4f6c376d4f88cb463a114e7f7b987072b010f24'

# Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def simulate_ai_analysis(filename):
    """Simulate AI analysis with random results"""
    time.sleep(2)  # Simulate processing time
    
    # Random tumor types and results
    tumor_types = ['Glioma', 'Meningioma', 'Pituitary Tumor', 'No Tumor Detected']
    statuses = ['Tumor Detected', 'No Tumor Detected', 'Suspicious Area Found']
    
    tumor_type = random.choice(tumor_types)
    status = random.choice(statuses)
    confidence = round(random.uniform(85.0, 99.5), 1)
    
    if tumor_type == 'No Tumor Detected':
        status = 'No Tumor Detected'
    
    return {
        'status': status,
        'tumor_type': tumor_type,
        'confidence': confidence,
        'filename': filename
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add timestamp to avoid filename conflicts
        timestamp = str(int(time.time()))
        filename = f"{timestamp}_{filename}"
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Simulate AI analysis
        analysis_result = simulate_ai_analysis(filename)
        
        return render_template('index.html', 
                             result=analysis_result,
                             uploaded_file=filename)
    else:
        flash('Invalid file type. Please upload an image file.')    
        return redirect(url_for('index'))

@app.route('/download_report')
def download_report():
    # In a real implementation, this would generate and return a PDF
    flash('PDF report download functionality would be implemented here.')
    return redirect(url_for('index'))

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)


if __name__ == '__main__':
    app.run(debug=True)