from flask import Flask,render_template,request,session,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user
import time
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
app.secret_key = 'my_secret_key'

if(local_server):
    app.config["SQLALCHEMY_DATABASE_URI"] = parameters['local_uri']
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = parameters['prod_uri']
# START THE DATABASE
db.init_app(app)

# DEFINING THE DATABASE MODELS

class Loginusers(db.Model):
    login_id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50), nullable = False)
    password=db.Column(db.String(50), nullable = False)
    def set_password(self, password):
        self.password = password

    def check_password(self, password):
        if(self.password==password):
            return 1
        
# class LoginAdmin(db.Model):
#     login_id=db.Column(db.Integer,primary_key=True)
#     username=db.Column(db.String(50), nullable = False)
#     password=db.Column(db.String(50), nullable = False)
#     def set_password(self, password):
#         self.password = password

#     def check_password(self, password):
#         if(self.password==password):
#             return 1
        
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
    ptimer = db.Column(db.Time)

    # def __init__(self, p_category, p_name, p_price, p_desc, p_closing, p_started, ptimer):
    #     self.p_category = p_category
    #     self.p_name = p_name
    #     self.p_price = p_price
    #     self.p_desc = p_desc
    #     self.p_closing = p_closing
    #     self.p_started = p_started
    #     self.ptimer = datetime.strptime(ptimer, '%H:%M:%S').time()



class Users(db.Model):
    uid=db.Column(db.Integer,primary_key=True)
    uname=db.Column(db.String(20), nullable = False)
    unumber=db.Column(db.Integer,nullable=False)
    umail=db.Column(db.String(20), nullable = False)
    upass=db.Column(db.String(20),nullable = False)
    ucnfpass=db.Column(db.String(20), nullable = False)
    ucity=db.Column(db.String(20), nullable = False)



# class Admins(db.Model):
#     admin_id=db.Column(db.Integer,primary_key=True)
#     admin_name=db.Column(db.String(20), nullable = False)
#     admin_no=db.Column(db.Integer,nullable=False)
#     admin_email=db.Column(db.String(20), nullable = False)
#     admin_pass=db.Column(db.String(20),nullable = False)
#     admin_cnfm_pass=db.Column(db.String(20), nullable = False)

class Bidders(db.Model):
    bid=db.Column(db.Integer,primary_key=True)
    uid=pid=db.Column(db.Integer,nullable=False)
    pid=db.Column(db.Integer,nullable=False)
    bprice=db.Column(db.Integer,nullable=False)

@app.route('/')
def base_index():
    return render_template('index.html')

#This is after login route i.e user view
@app.route('/home.html')
def home():
    user=session.get('username')
    return render_template('productsrow.html', name2 = user , )

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
        pclosing_db = request.form.get('date')
       
       # Get bidding duration
        hours = request.form.get('hours')
        minutes = request.form.get('minutes')
        seconds = request.form.get('seconds')
        ptimer_db = f"{hours}:{minutes}:{seconds}"
        pstarted = datetime.now()
        # print("********************* timer values checking ******************")
        # print(ptimer_db)


        # Add to the Database
        entry = Products(pcategory = pcategory_db , pname = pname_db , pprice = pprice_db , pdesc = pdesc_db , pclosing = pclosing_db ,pstarted = datetime.now(),ptimer=ptimer_db)
        # entry = Products(pcategory = pcategory_db , pname = pname_db , pprice = pprice_db , pdesc = pdesc_db , pclosing = pclosing_db ,pstarted = datetime.now())
        # entry = Products(pcategory_db ,pname_db , pprice_db ,pdesc_db , pclosing_db , pstarted, ptimer_db)


        db.session.add(entry)
        db.session.commit()

    return render_template('sampleseller.html')

@app.route('/buyer')
def buyer():
    # buyer = "gurav"
    current_user=session.get('username')
    #current_userId=session.get('id')
    query=db.engine.execute(f"SELECT * FROM `products`;")
    user = db.session.execute(f"SELECT uid FROM `users` WHERE uname=:name;", {'name': current_user}).fetchone()
    user_id = user[0]

    return render_template('samplehome.html',products = query,name2=current_user,id=user_id)


@app.route('/about.html')
def about():
    return render_template('about.html')   


@app.route('/login', methods=['GET', 'POST'])
def login():
    if(request.method == 'POST'):
        username  = request.form.get('username')
        password = request.form.get('password')
        # print(username,password)
        user = Users.query.filter_by(uname=username).first()
        # To add user in database
        userDB=Loginusers(username=username,password=password)
        # db.session.add(userDB)
        # db.session.commit()

        if user:
            session['username'] = user.uname
            return redirect(url_for('buyer'))
        
        
        return render_template('login.html')


    return render_template('login.html')  

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

@app.route('/signup.html', methods = ['GET','POST'])
def signup():
    if(request.method == 'POST'):
        
        uname_db = request.form.get('user_name')
        unumber_db = request.form.get('user_phone')
        umail_db = request.form.get('user_email')
        ucity_db = request.form.get('user_city')
        upass_db = request.form.get('password')
        ucnfpass_db = request.form.get('cnfPassword')

        entry = Users( uname = uname_db , unumber = unumber_db , umail = umail_db , upass = upass_db , ucnfpass = ucnfpass_db , ucity = ucity_db)

        # Check if the email already exists in the database
        # Query the database for a user with a specific email address
        user = Users.query.filter_by(umail=umail_db).first()
        print(user)
        if user:
            flash('Email already exists in the database')
            print("user exists")
            return render_template('signup.html')
        else :
            db.session.add(entry)
            db.session.commit()
            flash("Signup Success Please Login","success")
            return render_template('signup.html')


    return render_template('signup.html')

@app.route('/wologin.html')
def wologin():
    return render_template('wologin.html')


#Admin related stuff
@app.route('/adminhome')
def adminhome():
    total_users = Users.query.count()
    total_products = Products.query.count()
    total_bidders = Bidders.query.count()
    total_queries = Contacts.query.count()
    return render_template('adminhome.html', total_users=total_users, total_products=total_products, bidders=total_bidders, queries = total_queries)



@app.route('/AdminLogin', methods=['GET', 'POST'])
def adminlogin():
    if(request.method == 'POST'):
        username  = request.form.get('username')
        password = request.form.get('password')
        # print(username,password)
        admin1="omgurav"
        admin1_pass="om123"
        admin2="prayog"
        admin2_pass="prayog123"
        if (username==admin1 and password==admin1_pass) :
            flag=1
        if (username==admin2 and password==admin2_pass ) :
            flag=1    

        if flag:
            return redirect(url_for('adminhome'))
        
        
        return render_template('adminlogin.html')


    return render_template('adminlogin.html')  


@app.route('/product/<int:pid>', methods = ['GET','POST'])
# @login_required
def show_product(pid):
    print("Yes")
    # product = Products.query.get('pid')
    product = db.session.execute(f"SELECT * FROM `products` WHERE pid=:pid;", {'pid': pid}).fetchone()
    if product is None:
        return 'Product not found', 404
    
    current_user=session.get('username')
    #current_userId=session.get('id')
    # query=db.engine.execute(f"SELECT * FROM `products`;")
    user = db.session.execute(f"SELECT uid FROM `users` WHERE uname=:name;", {'name': current_user}).fetchone()
    curr_bid = db.session.execute(f"SELECT max(bprice) FROM `bidders` where pid=:pid;", {'pid': pid}).fetchone()
    user_id = user[0]
    print(curr_bid[0])
    if(curr_bid[0] is None):
        latest_bid = 0
    else:
        latest_bid = int(curr_bid[0])

    
    # print("/////////////////////////////////****************")
    # print(new_bid)
    if(request.method == 'POST' ):
        bprice_db = int(request.form.get('bid'))
        
        
        if(latest_bid < bprice_db):
            pid_db=pid
            entry = Bidders( uid = user_id , bprice=bprice_db, pid=pid_db)
            db.session.add(entry)
            db.session.commit()
    
    return render_template('product.html', product=product,id = user_id,curr_bid=latest_bid)

@app.route('/sorry')
def sorry():
    render_template('sorry.html')


@app.route('/myproduct/<int:uid>')
# @login_required
def my_products(uid):
    print("Yes")
    # product = Products.query.get('pid')
    my_product = db.session.execute(f"SELECT * FROM `bidders` WHERE uid=:uid;", {'uid': uid})
    #my_product1 = db.session.execute(f"SELECT pid FROM `bidders` WHERE uid=:uid;", {'uid': uid}).fetchone()
    #print(my_product1[0])

    
    
    
    return render_template('myproduct.html', bidders=my_product)
    

@app.route('/myprofile/<int:uid>')
def my_profile(uid):
    #print("\nYes",uid)
    my_Profile = db.session.execute(f"SELECT * FROM `users` WHERE uid=:uid;", {'uid': uid}).fetchone()
    if my_Profile is None:
        print("Hello")
        return 'Profile not found', 404
    
    print(my_Profile.uname)
        
    
    return render_template('myprofile.html',profile=my_Profile)



@app.route('/editprofile/<int:uid>', methods = [ 'GET' , 'POST'])
def edit_profile(uid): 
    if(request.method == 'POST'):
        # Add Entry TO Database
        # contact_no , name, email, pNumber, message, dt 
        # the first name is entry in the database and another name is for Html page 
        new_name  = request.form.get('name')
        new_email = request.form.get('email')
        new_phone = request.form.get('phone')


        db.session.execute('UPDATE `users` SET uname = :name, umail = :email, unumber = :phone WHERE uid = :id', {'name': new_name, 'email': new_email, 'phone': new_phone, 'id': uid})
        db.session.commit()

        flash('Your Details Updated Successfully','success')
        # return redirect(url_for('edit_profile', uid=uid))
        return redirect(url_for('my_profile', uid=uid))
        #Above is the function Bro.
        

    return render_template('editprofile.html',uid=uid)


@app.route('/admin/users')
def adminusers():
    admin_users = db.engine.execute(f"SELECT * FROM `users`;")
    return render_template('users-admin.html', users=admin_users)

@app.route('/admin/edituser/<int:uid>', methods = [ 'GET' , 'POST'])
def edit_user(uid): 
    if(request.method == 'POST'):
        # Add Entry TO Database
        # contact_no , name, email, pNumber, message, dt 
        # the first name is entry in the database and another name is for Html page 
        new_name  = request.form.get('username')
        new_email = request.form.get('email')
        new_phone = request.form.get('mobile')
        new_city = request.form.get('city')



        db.session.execute('UPDATE `users` SET uname = :name, umail = :email, unumber = :phone, ucity = :city WHERE uid = :id', {'name': new_name, 'email': new_email, 'phone': new_phone, 'id': uid,'city':new_city })
        db.session.commit()

        flash('Your Details Updated Successfully','success')
        # return redirect(url_for('edit_profile', uid=uid))
        # return redirect(url_for('my_profile', uid=uid))
        #Above is the function Bro.
        

    return render_template('edituser.html',uid=uid)


@app.route('/admin/products')
def adminproducts():
    admin_products = db.engine.execute(f"SELECT * FROM `products`;")
    return render_template('product-admin.html', products=admin_products)


@app.route('/admin/bidders')
def adminbidders():
    admin_bidders = db.engine.execute(f"SELECT * FROM `bidders`;")
    return render_template('bidders-admin.html', bidders=admin_bidders)


@app.route('/admin/contacts')
def admincontacts():
    admin_contacts = db.engine.execute(f"SELECT * FROM `contacts`;")
    return render_template('contact-admin.html', contacts=admin_contacts)


if __name__ == "__main__":
    app.run(debug = True,port = 5005)
