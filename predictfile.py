import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
import keras, sys
import numpy as np
from PIL import Image
from keras.models import Sequential, load_model

# data info
classes = ["monkey", "crow", "boar"]
num_classes = len(classes)
image_size = 50

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTEMSIONS = set(['png', 'jpg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTEMSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('ファイルがありません')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('ファイルがありません')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # モデルのロード
            model = load_model('./animal_cnn_aug.h5')

            image = Image.open(filepath)
            image = image.convert('RGB')
            image = image.resize((image_size, image_size))
            data = np.asarray(image)
            X = []
            X.append(data)
            X = np.asarray(X)

            result = model.predict([X])[0]
            # 最大値が入っている添え字を返却
            predicted = result.argmax()
            percentage = int(result[predicted] * 100)

            return "label: " + classes[predicted] + ", result: " + str(percentage) + "%"

            ## return redirect(url_for('uploaded_file',filename=filename))
    return '''
            <!doctype html>
            <html><head>
            <meta charset="UTF-8"
            <title>Upload new File</title>
            </head>
            <body>
            <h1>ファイル判定</h1>
            <form method=post enctype=multipart/form-data>
            <p><input type=file name=file></p>
            <input type=submit value=Upload>
            </form></body></html>
            '''


from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
