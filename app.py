import os
from flask import *
from PIL import Image, ImageOps
from flask import request
import numpy as np
import tensorflow.keras
import sqlite3


app = Flask(__name__)

#Directory to store uploaded images
app.config["IMAGE_UPLOADS"] = "C:/Users/Utkarsh/Desktop/project/Potholes Detection Project/uploads"

# Load the model
model = tensorflow.keras.models.load_model('keras_model.h5')

#Default page of web application
@app.route('/')
def hello():
    return render_template('login.html')

#Login User
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = sqlite3.connect("users.db")
        error = None
        user = db.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        )
        
        if user is None:
            error = 'Incorrect username.'

        for row in user:
            checkpassword=row[1]

        if error is None and username!="admin" :
            return render_template('test.html')

        if error is None and username=='admin' :
            con = sqlite3.connect("users.db")  
            db=con.cursor()
            db.execute('select name,phone,street,city,depth,description from potholes ')
            return render_template('admin.html',items=db.fetchall())
    return render_template('login.html')


@app.route('/query', methods=['GET', 'POST'])
def query():
    if request.method == 'POST':
       
            area=request.form['area']
            print('in')
            con = sqlite3.connect("users.db")  
            db=con.cursor()
            db.execute('select * from potholes where UPPER(street) = UPPER(?) ',(area,))
            return render_template('admin.html',items=db.fetchall())

@app.route('/del', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        mob=request.form['mob']
        con = sqlite3.connect("users.db")  
        db=con.cursor()
        db.execute('delete from potholes where phone = ? ',(mob,))
        return render_template('admin.html',items=db.fetchall())
        



#Register New Users
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            con = sqlite3.connect("users.db")  
            db=con.cursor()
            db.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            con.commit()
        except:
            con.rollback()
        finally:
            return render_template('login.html')
            con.close()




#Test the uploaded image
@app.route('/test', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'image' in request.files:
            name=request.form['name']
            phone=request.form['phone']
            street=request.form['street']
            city=request.form['city']
            depth=request.form['depth']
            description=request.form['desc']
            latitude=request.form['latitude']
            longitude=request.form['longitude']

            tmp="C:/Users/Utkarsh/Desktop/project/Potholes Detection Project/uploads"
            data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
            img=request.files['image']
            img.save(os.path.join(app.config["IMAGE_UPLOADS"], img.filename))
            image=Image.open(tmp+'/'+img.filename)
            size = (224, 224)
            image = ImageOps.fit(image, size, Image.ANTIALIAS)
            image_array = np.asarray(image)
            normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
            data[0] = normalized_image_array
            prediction = model.predict(data)
            ans=prediction[0][0]
            if round(ans,3)>0.70 :
                con = sqlite3.connect("users.db")  
                db=con.cursor()
                db.execute('INSERT INTO potholes VALUES (?,?,?,?,?,?,?,?)', (name, phone,street,city,depth,description,latitude,longitude))
                con.commit()
                con.close()
                return render_template('success.html')
            return render_template('fail.html')


if __name__ == '__main__':
    app.run(debug=True)