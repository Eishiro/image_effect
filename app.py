import os
from flask import Flask, render_template, request,redirect, send_from_directory,url_for
from datetime import datetime

# ファイル名をチェックする関数
from werkzeug.utils import secure_filename
# 画像のダウンロード
from flask import send_from_directory

app = Flask(__name__)



@app.route('/home')
def home():
    return 'HOME!'

@app.route('/hello/<name>')
def hello(name = None):
    return render_template('hello.html', name = name)




UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'txt', 'png', 'jpg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST', 'GET'])
def upload_file():
    #if request.method == 'GET':
    #    return render_template('index.html')

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('ファイルがありません')
            return redirect(request.url)

        #Get file object
        file = request.files['file']
        print ("aaaaa"+file.name+ ('\n'))

        # ファイル名がなかった時の処理
        if file.filename == '':
            flash('ファイルがありません')
            return redirect(request.url)

        # File Check
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
