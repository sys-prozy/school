from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.secret_key = 'secret_key_here'

# Max number of captives
MAX_CAPTIVES = 10

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Route to upload and handle captives list
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        # Save the file
        if file and allowed_file(file.filename):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # Read and validate the file
            with open(filepath, 'r') as f:
                captives = [line.strip() for line in f.readlines() if line.strip()]
                
            if len(captives) > MAX_CAPTIVES:
                flash(f'Maximum {MAX_CAPTIVES} captives are allowed.')
                return redirect(request.url)

            # Display captives or handle logic
            return render_template('captives.html', captives=captives)

    return render_template('upload.html')

# Allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'txt'

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True, host='0.0.0.0')
