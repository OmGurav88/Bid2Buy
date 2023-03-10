from flask import Flask,render_template,request,session,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user
from datetime import datetime
import json 
# from flask_mail import Mail


# USE FOR USING DATABASE
db = SQLAlchemy()
local_server = True
with open('config.json', 'r') as con:
    parameters = json.load(con)["params"]

# WSGI Application
app = Flask(__name__)

if(local_server):
    app.config["SQLALCHEMY_DATABASE_URI"] = parameters['local_uri']
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = parameters['prod_uri']
# START THE DATABASE
db.init_app(app)
# DEFINING THE DATABASE OF `contacts`

class Contacts(db.Model):
    contact_id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50), nullable = False)
    email=db.Column(db.String(50), nullable = False)
    pNumber=db.Column(db.Integer(), nullable = False)
    message=db.Column(db.String(200), nullable = False)
    dt=db.Column(db.String(100))


class Products(db.Model):
    pid=db.Column(db.Integer,primary_key=True)
    pcategory=db.Column(db.String(20), nullable = False)
    pname=db.Column(db.String(50), nullable = False)
    pprice=db.Column(db.Integer(), nullable = False)
    pdesc=db.Column(db.String(200), nullable = False)
    pclosing=db.Column(db.String(100), nullable = False)
    pstarted=db.Column(db.String(100))


@app.route('/')
def base_index():
    return render_template('index.html')



@app.route('/home.html')
# @login_required
def home():
    name = "Prayog"
    return render_template('home.html', name2 = name)

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/seller.html',methods = ['GET' , 'POST'])
def seller():
    if(request.method == 'POST'):
        # Add Entry TO Database
        # contact_no , name, email, pNumber, message, dt 
        # the first name is entry in the database and another name is for Html page 
        pcategory_db  = request.form.get('category')
        pname_db = request.form.get('productName')
        pprice_db = request.form.get('price')
        pdesc_db = request.form.get('msg')
        pclosing_db = request.form.get('datetime')

        # Add to the Database
        entry = Products(pcategory = pcategory_db , pname = pname_db , pprice = pprice_db , pdesc = pdesc_db , pclosing = pclosing_db ,pstarted = datetime.now())
        db.session.add(entry)
        db.session.commit()

    return render_template('seller.html')

@app.route('/buyer')
def buyer():
    buyer = "gurav"
    query=db.engine.execute(f"SELECT * FROM `products`")
    return render_template('buyer.html',products = query,name2=buyer)

@app.route('/about.html')
def about():
    return render_template('about.html')   

@app.route('/login.html')
def login():
    return render_template('login.html')  

@app.route('/home.html')
def afterlogin():
    return render_template('home.html')

@app.route('/contact.html', methods = [ 'GET' , 'POST'])
def contact(): 
    if(request.method == 'POST'):
        # Add Entry TO Database
        # contact_no , name, email, pNumber, message, dt 
        # the first name is entry in the database and another name is for Html page 
        name_db  = request.form.get('name')
        email_db = request.form.get('email')
        pNumber_db = request.form.get('phone')
        message_db = request.form.get('msg')

        # Add to the Database
        entry = Contacts(name = name_db , email = email_db , pNumber = pNumber_db , message = message_db , dt = datetime.now())
        db.session.add(entry)
        db.session.commit()

    return render_template('contact.html')

@app.route('/post.html')
def post():
    return render_template('post.html')

@app.route('/prayog')
def prayog():
    return render_template('prayog.html')

@app.route('/signup.html')
def signup():
    return render_template('signup.html')

# @app.route('/login')
# def aftersignup():
#     return render_template('login.html')

if __name__ == "__main__":
    app.run(debug = True,port = 5005)
