from flask import Flask, request, render_template, send_file
from utils import add_watermark

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return "No file part"
    file = request.files['image']
    if file.filename == '':
        return "No selected file"
    if file:
        watermark_text = request.form['watermark']
        watermarked_image = add_watermark(file.stream, watermark_text)
        return send_file(watermarked_image, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True) 