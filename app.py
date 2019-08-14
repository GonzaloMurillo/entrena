#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
from flask import Flask, flash, request, redirect, url_for, render_template
from flask import send_from_directory
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = {'tcx'}

app=Flask(__name__)
app.secret_key = '12sa__eeerr332323'
UPLOAD_FOLDER = 'static/upload' # This is referred to the root of the app
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

## This is a function that determines if a file is one of the ALLOWED_EXTENSIONS
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# The root page
@app.route('/',methods = ['GET','POST'])
def index():
    
    file_names=[]
    errors=False
    if request.method == 'POST':
        if len(request.form["email"])<1:
            flash('Email no especificado')
            errors=True
        
        if len(request.form["fechanacimiento"])<1:
            flash('Fecha nacimiento no especificada')
            errors=True

        if  len(request.files['tcxfiles[]'].read())<1:
            flash('Fichero .tcx no especificado')
            errors=True

        if errors:
            return redirect(request.url)
        files = request.files.getlist("tcxfiles[]")
        # if user does not select file, browser also
        # submit an empty part without filename
        for each_file in files:
            if each_file and allowed_file(each_file.filename):
                filename = secure_filename(each_file.filename)
                file_names.append(filename)
                each_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        if not errors:
            return redirect(url_for('tcx_analysis',tcx_files=file_names,email=request.form["email"]))
    return render_template('basic.html')

@app.route('/tcx_analysis/<tcx_files>/<email>')
def tcx_analysis(tcx_files,email):
    print(tcx_files)
    return ("Hola"+email+tcx_files)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if(__name__== "__main__"):
    app.run(debug=True)
