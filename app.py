from flask import Flask,render_template,url_for,request,redirect,jsonify

from flask_jwt_extended import JWTManager,create_access_token,get_jwt_identity,jwt_required
from werkzeug.utils import secure_filename
from models import db,Image
from config import Config
from flask_restful import Resource,Api
import os
from flask_cors import CORS
app=Flask(__name__)
CORS(app)
from flask_sqlalchemy import SQLAlchemy

import mysql.connector
dbname=mysql.connector.connect(
    host="localhost",
    user='root',
    password='root',
    database='mysql',
    port=3306)

app.config.from_object(Config)

# Change this!
jwt=JWTManager(app)

#app.config['UPLOAD_FOLDER'] = 'uploads/'
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db=SQLAlchemy(app)



api=Api(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

@app.route('/upload',methods=['GET','POST'])
#@jwt_required()
def upload():
    if request.method=='POST':
        file=request.files['file']
        if file:
            filename=file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            new_Image=Image(filename=filename)
           
            return redirect(url_for('result',filename=filename))
        else:
            return 'File not found tuui'
        
    return render_template('upload.html')
@app.route('/index')
def index():
    return render_template('index.html')
@app.route('/result')
#@jwt_required()
def result():
    filename=request.args.get('filename')
    return render_template('result.html',filename=filename)

@app.route('/login',methods=['GET','POST'])
def login():
    
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if username != 'root' or password != 'root':
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200
if __name__=='__main__':  
    with app.app_context():
        db.create_all()
    app.run(debug=True)