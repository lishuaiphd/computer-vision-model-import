from flask import Flask, render_template, request, send_file, redirect, url_for, flash
import os
from inference import process_image_to_gliffy

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXT = {'png', 'jpg', 'jpeg', 'tiff', 'bmp'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'replace-this-with-a-secure-secret'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
    return redirect(request.url)


f = request.files['file']
if f.filename == '':
    flash('No selected file')
return redirect(request.url)
if f and allowed(f.filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
f.save(filepath)
out_path = process_image_to_gliffy(filepath)
if out_path:
    return send_file(out_path, as_attachment=True)
else:
    flash('Processing failed')
return redirect(request.url)
return render_template('index.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
