 
import os

from flask import Flask, render_template, request, jsonify, flash, send_file
from werkzeug.utils import secure_filename
from .conversion_utils import print_pages
import datetime, base64
from PyPDF2 import PdfFileMerger
import io

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='LJD7qGdozM2we6ed',
        ALLOWED_EXTENSIONS = set(['pdf']),
        MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    )
    
    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/upload',methods=['POST'])
    def upload():
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file')
                return render_template('index.html')
            file = request.files['file']
            lang = request.form['lang']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No file selected')
                return render_template('index.html')
            if file and allowed_file(file.filename):
                # filename = secure_filename(file.filename)
                # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                text = print_pages(file.stream.read(),lang,path=False)
                return render_template('result.html',
                        data=datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d"),
                        resulttext=text, base64text=base64.b64encode(text.encode('utf-8')).decode())

    @app.route('/join',methods=['POST'])
    def join():
        if request.method == 'POST':

            if 'files[]' not in request.files:
                flash('No files')
                return render_template('index.html')

            merger = PdfFileMerger()
            files = request.files.getlist('files[]')
            files.sort(key=lambda x: x.filename) # sort by name
            if len(files)>1:
                for file in files:
                    if file and allowed_file(file.filename):
                        merger.append(file.stream)
                
                outputfile = io.BytesIO()
                merger.write(outputfile)
                outputfile.seek(0)
                return send_file(
                    outputfile,
                    as_attachment=True,
                    attachment_filename="merge{}.pdf".format(datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d")))
            else:
                flash('Only one file selected')
                return render_template('index.html')


    return app