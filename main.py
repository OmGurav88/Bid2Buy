from flask import Flask,render_template,request,session,redirect,url_for,flash,Response,send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user
from datetime import datetime, timedelta
from datetime import datetime
import json 
import os
from werkzeug.utils import secure_filename
from PIL import Image
import random
import string
from flask import render_template, request, flash, redirect, url_for
import re
<<<<<<< Updated upstream
import qrcode


=======
import hashlib
>>>>>>> Stashed changes

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


class Loginusers(db.Model):
    login_id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50), nullable = False)
    password=db.Column(db.String(50), nullable = False)
    def set_password(self, password):
        self.password = password

    def check_password(self, password):
        if(self.password==password):
            return 1
        
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
    pstarted=db.Column(db.String(100), nullable = True )
    ptimer = db.Column(db.Time)
    uid=db.Column(db.Integer, nullable = False)
    pbid=db.Column(db.Integer , nullable = False)
    pimageName = db.Column(db.String(50), nullable=False)


class Users(db.Model):
    uid=db.Column(db.Integer,primary_key=True)
    uname=db.Column(db.String(20), nullable = False)
    unumber=db.Column(db.String(20),nullable=False)
    umail=db.Column(db.String(20), nullable = False)
    upass=db.Column(db.String(20),nullable = False)
    ucnfpass=db.Column(db.String(20), nullable = False)
    ucity=db.Column(db.String(20), nullable = False)
    

class Bidders(db.Model):
    bid=db.Column(db.Integer,primary_key=True)
    uid=pid=db.Column(db.Integer,nullable=False)
    pid=db.Column(db.Integer,nullable=False)
    bprice=db.Column(db.Integer,nullable=False)


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50), nullable=False)


def generate_qr(price):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(f'Price: {price}')
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    return img
    
@app.route('/')
def base_index():
    return render_template('index.html')

#This is after login route i.e user view
@app.route('/home.html')
def home():
    user=session.get('username')
    
    return render_template('productsrow.html', name2 = user ,)

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/seller.html',methods = ['GET' , 'POST'])
def seller():
    current_user=session.get('username')
    user = db.session.execute(f"SELECT uid FROM `users` WHERE uname=:name;", {'name': current_user}).fetchone()
    user_id = user[0]
    if(request.method == 'POST'):
      
        pcategory_db  = request.form.get('category')
        pname_db = request.form.get('productName')
        pprice_db = request.form.get('price')
        pdesc_db = request.form.get('msg')
        pstarted_db = request.form.get('startingdatetime')
        pclosing_db = request.form.get('endingdatetime')
        uid_db = user_id
        pbid_db = request.form.get('price')
        
        
       
       
        file = request.files['file']
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # Save filename to database
        

        # Add to the Database
        entry = Products(pcategory = pcategory_db , pname = pname_db , pprice = pprice_db , pdesc = pdesc_db , pclosing = pclosing_db ,pstarted = pstarted_db,uid=uid_db,pbid=pbid_db,pimageName=filename)
        # entry = Products(pcategory = pcategory_db , pname = pname_db , pprice = pprice_db , pdesc = pdesc_db , pclosing = pclosing_db ,pstarted = datetime.now())
        # entry = Products(pcategory_db ,pname_db , pprice_db ,pdesc_db , pclosing_db , pstarted, ptimer_db)


        db.session.add(entry)
        db.session.commit()
        flash('Your Product added Successfully!!')

    return render_template('sampleseller.html',user_id=user_id,current_page='seller',id=user_id)

@app.route('/buyer')
def buyer():
    # buyer = "gurav"
    current_user=session.get('username')
    # session['user_id'] = current_user.id
    # id=session.get('user_id')
    #current_userId=session.get('id')
    query1=db.engine.execute(f"SELECT * FROM `products` WHERE pclosing-Now()>0 AND pstarted-Now()<0 order by pclosing desc;")
    query2=db.engine.execute(f"SELECT * FROM `products` WHERE pclosing-Now()<0 order by pclosing desc;")
    query3=db.engine.execute(f"SELECT * FROM `products` WHERE pstarted-Now()>0 order by pclosing desc;")
    user = db.session.execute(f"SELECT uid FROM `users` WHERE uname=:name;", {'name': current_user}).fetchone()
    user_id = user[0]


    return render_template('samplehome.html',active = query1,outdated=query2,future=query3,name2=current_user,id=user_id,current_page='buyer')


@app.route('/about.html')
def about():
    return render_template('about.html')   


@app.route('/login', methods=['GET', 'POST'])
def login():
    if(request.method == 'POST'):
        username  = request.form.get('username')
        password = request.form.get('password')
   
        user = Users.query.filter_by(uname=username).first()
        user_pass = Users.query.filter_by(upass=password).first()
        # To add user in database
        userDB=Loginusers(username=username,password=password)

        if user and user_pass:
            session['username'] = user.uname
            return redirect(url_for('buyer'))
        
        flash('Username or Password Incorrect.', 'warning')
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

    return render_template('index.html')

@app.route('/post.html')
def post():
    return render_template('post.html')

def is_valid_email(email):
    pattern = r'[^@]+@[^@]+\.[^@]+'  # Regular expression pattern to validate email
    return re.match(pattern, email) is not None

def is_valid_password(password):
    pattern = r'^(?=.*[A-Za-z])(?=.*\d).{8,}$'  # Regular expression pattern to validate password
    return re.match(pattern, password) is not None

def is_valid_mobile_number(number):
    pattern = r'^\d{10}$'
    return re.match(pattern, number) is not None

@app.route('/signup.html', methods = ['GET','POST'])
def signup():
    if(request.method == 'POST'):
        
        uname_db = request.form.get('user_name')
        unumber_db = request.form.get('user_phone')
        umail_db = request.form.get('user_email')
        ucity_db = request.form.get('user_city')
        upass_db = request.form.get('password')
        ucnfpass_db = request.form.get('cnfPassword')
        
        if upass_db!=ucnfpass_db :
            flash('Please enter same password')
            return render_template('signup.html')

        hashed_password = hashlib.sha256(upass_db.encode()).hexdigest()

        entry = Users( uname = uname_db , unumber = unumber_db , umail = umail_db , upass =hashed_password , ucnfpass = hashed_password , ucity = ucity_db)
        
        
        user = Users.query.filter_by(uname=uname_db).first()
        if user:
            flash('Username already exists in the database')
            print("user exists")
            return render_template('signup.html')
        
        email = Users.query.filter_by(umail=umail_db).first()
        if email:
            flash('Eamil already exists in the database')
            print("Email exists")
            return render_template('signup.html')


        if not is_valid_mobile_number(unumber_db):
            flash('Invalid Mobile number')
            return render_template('signup.html')
        
        if not is_valid_email(umail_db):
            flash('Invalid email address')
            return render_template('signup.html')

        # Validate password
        if not is_valid_password(upass_db):
            flash('Password should contain atleast one uppercase/lowercase ,atleast one digit, minimum length of 8 characters.')
            return render_template('signup.html')
 
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
        flag=0
        if (username==admin1 and password==admin1_pass) :
            flag=1
        if (username==admin2 and password==admin2_pass ) :
            flag=1    

        if flag:
            return redirect(url_for('adminhome'))
        
        flash('Username or Password Incorrect.', 'danger')
        flash('Please Contact Admin.', 'warning')
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
        latest_bid = product.pprice
    else:
        latest_bid = int(curr_bid[0])

    
    # print("/////////////////////////////////****************")
    # print(new_bid)
    if(request.method == 'POST' ):
        bprice_db = int(request.form.get('bid'))
        # pbid_db = int(request.form.get('bid'))
        pstarted = product.pclosing
        # print(product.pstarted)
        # print(product.pclosing)
        now = datetime.now()
        formatted_pstarted = pstarted.strftime('%Y-%m-%d %H:%M:%S')
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        # print(formatted_date - formatted_pstarted)

        date1 = datetime.strptime(formatted_pstarted, '%Y-%m-%d %H:%M:%S')
        date2 = datetime.strptime(formatted_date, '%Y-%m-%d %H:%M:%S')

        time_difference_seconds = (date1 - date2).total_seconds()

        if(time_difference_seconds <= 0):
            flash('Sorry!! You cant Bid Now')
            flash('Bid Time is Expired')
            return render_template('product.html', product=product,id = user_id,curr_bid=latest_bid)
        if(user_id == product.pbuid):
            flash('Sorry!! You cant Bid Now')
            flash('You Have Highest Bid.')
            return render_template('product.html', product=product,id = user_id,curr_bid=latest_bid)
        if(user_id == product.uid):
            flash('Sorry!! You can\'t Bid on Your Product.')
            return render_template('product.html', product=product,id = user_id,curr_bid=latest_bid)

        
        if(latest_bid < bprice_db):
            pid_db=pid
            entry = Bidders( uid = user_id , bprice=bprice_db, pid=pid_db)
            db.session.add(entry)
            db.session.execute('UPDATE `products` SET pbid = :bid , pbuid=:uid WHERE pid =:pid;', { 'bid': bprice_db,'pid':pid,'uid':user_id})
            
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
    my_product = db.session.execute(f"SELECT DISTINCT pid FROM `bidders` WHERE uid=:uid;", {'uid': uid})

    
    
    return render_template('myproduct.html', bidders=my_product,current_page='myproduct',id=uid )
    
@app.route('/admin')
def admin():
    return render_template('adminhome.html')

@app.route('/myprofile/<int:uid>')
def my_profile(uid):
    #print("\nYes",uid)
    my_Profile = db.session.execute(f"SELECT * FROM `users` WHERE uid=:uid;", {'uid': uid}).fetchone()
    if my_Profile is None:
        print("Hello")
        return 'Profile not found', 404
    
    print(my_Profile.uname)
        
    
    return render_template('myprofile.html',profile=my_Profile,uid=uid,current_page='myprofile')

@app.route('/editprofile/<int:uid>', methods = [ 'GET' , 'POST'])
def edit_profile(uid): 
    if(request.method == 'POST'):
        # Add Entry TO Database
        # contact_no , name, email, pNumber, message, dt 
        # the first name is entry in the database and another name is for Html page 
        new_name  = request.form.get('username')
        new_email = request.form.get('email')
        new_phone = request.form.get('mobile')
        new_pass = request.form.get('password')
        new_city = request.form.get('city')



        db.session.execute('UPDATE `users` SET uname = :name, umail = :email, unumber = :phone, upass = :new_pass ,ucity = :city WHERE uid = :id', {'name': new_name, 'email': new_email, 'phone': new_phone, 'id': uid,'city':new_city })
        db.session.commit()

        flash('Your Details Updated Successfully','success')
        return redirect(url_for('edit_profile', uid=uid))
        # return redirect(url_for('/admin'))
        # return render_template('adminhome',uid=uid)
        

    return render_template('editprofile.html',uid=uid)


@app.route('/admin/users')
def adminusers():
    admin_users = db.engine.execute(f"SELECT * FROM `users`;")
    return render_template('users-admin.html', users=admin_users)

# @app.route('/admin/edituser/<int:uid>', methods = [ 'GET' , 'POST'])
# def edit_user(uid): 
#     if(request.method == 'POST'):
#         # Add Entry TO Database
#         # contact_no , name, email, pNumber, message, dt 
#         # the first name is entry in the database and another name is for Html page 
#         new_name  = request.form.get('username')
#         new_email = request.form.get('email')
#         new_phone = request.form.get('mobile')
#         new_pass = request.form.get('new_password')
#         new_city = request.form.get('city')
#         print("++++++++++++++++++++++++++=\n")
#         print(new_name," ",new_email," ",new_pass," ",new_phone)



#         db.session.execute('UPDATE `users` SET uname = :new_name, umail = :new_email, unumber = :new_phone, upass = :new_pass , ucnfpass:new_pass ,ucity = :new_city WHERE uid = :id', {'name': new_name, 'email': new_email, 'phone': new_phone, 'id': uid,'ucnfpass':new_pass,'city':new_city })
#         db.session.commit()

#         flash('Your Details Updated Successfully','success')
#         return render_template('adminhome.html')
#         # return redirect(url_for('edit_profile', uid=uid))
#         # return redirect(url_for('my_profile', uid=uid))
#         #Above is the function Bro.
        

#     return render_template('edituser.html',uid=uid)
@app.route('/admin/edituser/<int:uid>', methods=['GET', 'POST'])
def edit_user(uid): 
    if request.method == 'POST':
        # Get form data
        new_name = request.form.get('username')
        new_email = request.form.get('email')
        new_phone = request.form.get('mobile')
        new_pass = request.form.get('new_password')
        new_city = request.form.get('city')

        # Update user in database
        db.session.execute('UPDATE `users` SET uname = :new_name, umail = :new_email, unumber = :new_phone, upass = :new_pass, ucnfpass = :ucnfpass, ucity = :new_city WHERE uid = :uid',
                            {'new_name': new_name, 'new_email': new_email, 'new_phone': new_phone, 'new_pass': new_pass, 'ucnfpass': new_pass, 'new_city': new_city, 'uid': uid})
        db.session.commit()

        flash('Your details have been updated successfully', 'success')
        return redirect(url_for('edit_user', uid=uid))
        # return redirect(url_for('/admin/users', uid=uid))
        

    # Get user data from database and render form
    # user = Users.query.filter_by(uid=uid).first()
    return render_template('edituser.html', uid=uid)


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

@app.route('/admin/viewproduct/<int:pid>')
def viewproducts(pid):
    
    view_product = db.session.execute(f"SELECT * FROM `products` WHERE pid = :pid;", {'pid': pid}).fetchone()
    # latest_bid = int(curr_bid[0])
    print(view_product.pprice)
    if(view_product.pbid > view_product.pprice):
        view_bidders = db.session.execute(f"SELECT * FROM `bidders` WHERE pid=:pid ORDER BY bprice desc;", {'pid': pid})
        curr_bid = db.session.execute(f"SELECT max(bprice) FROM `bidders` where pid=:pid;", {'pid': pid}).fetchone()

        latest_bid = int(curr_bid[0])
        return render_template('viewproductadmin.html',bidders=view_bidders,curr_bid=latest_bid,product=view_product)
    else:
        return render_template('viewproductadmin.html',curr_bid=view_product.pbid,product=view_product)

@app.route('/productonbid/<int:uid>')
def view_productOnBid(uid):
    productOnBid = db.session.execute(f"SELECT * FROM `products` WHERE uid=:uid;", {'uid': uid})
    return render_template('productonbid.html',product=productOnBid,id=uid,current_page='productonbid')



# @app.route('/auction')
# def auction():
#     # Calculate time remaining until auction ends
    
#     time_remaining = auction_end_time - datetime.now()

#     # Check if auction has ended
#     if time_remaining <= timedelta():
#         return render_template('auction_ended.html')

#     # Render auction template with time remaining
#     return render_template('auction.html', time_remaining=time_remaining)

@app.route('/sample/<int:pid>', methods = ['GET','POST'])
# @login_required
def sample(pid):
    print("Yes")
    # product = Products.query.get('pid')
    product = db.session.execute(f"SELECT * FROM `products` WHERE pid=:pid;", {'pid': pid}).fetchone()
    if product is None:
        return 'Product not found', 404
    
    
    
    return render_template('sample.html', product=product,)


@app.route('/user/viewproduct/<int:pid>')
def viewproductsuser(pid):
    current_user=session.get('username')
    user = db.session.execute(f"SELECT uid FROM `users` WHERE uname=:name;", {'name': current_user}).fetchone()
    
    user_id = user[0]
    view_bidders = db.session.execute(f"SELECT * FROM `bidders` WHERE pid=:pid and uid=:uid ORDER BY bprice desc;", {'pid': pid,'uid':user_id})
    curr_bid = db.session.execute(f"SELECT max(bprice) FROM `bidders` where pid=:pid;", {'pid': pid}).fetchone()
    view_product = db.session.execute(f"SELECT * FROM `products` WHERE pid = :pid;", {'pid': pid}).fetchone()
    latest_bid = int(curr_bid[0])
    return render_template('viewproductuser.html',bidders=view_bidders,curr_bid=latest_bid,product=view_product)


@app.route('/winproduct/<int:uid>')
# @login_required
def win_products(uid):
    print("Yes")
    # product = Products.query.get('pid')
    my_product = db.session.execute(f"SELECT * FROM `products` WHERE pbuid=:uid;", {'uid': uid})
    #my_product1 = db.session.execute(f"SELECT pid FROM `bidders` WHERE uid=:uid;", {'uid': uid}).fetchone()
    #print(my_product1[0])
    
    
    return render_template('winproduct.html', bidders=my_product,current_page='winproduct',id=uid )



#################################################################
# SAMPLE

@app.route('/sample.html', methods=['GET','POST'])
def upload():
    if(request.method == 'POST'):
        print("yes")
        file = request.files['file']
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # Save filename to database
        image = Image(filename=filename)
        db.session.add(image)
        db.session.commit()

    return render_template('sample.html')





@app.route('/get_image')
def getimage():
    
    # name=db.session.execute("SELECT * FROM `image` WHERE id=:id;", {'id': id}).fetchone()
    return render_template('sorry.html')


@app.route('/productpayment/<int:pid>', methods = [ 'GET' , 'POST'])
def product_payment(pid): 
    product = db.session.execute(f"SELECT * FROM `products` WHERE pid=:pid;", {'pid': pid}).fetchone()   
    flash('Congratulations! You Won this product', 'success')
    return render_template('productpayment.html',uid=pid,product=product)
    
    
################################################################

@app.route('/search')
def search():
    query = request.args.get('q')
    # TODO: Implement search logic using the query parameter
    query = f"SELECT * FROM products WHERE name LIKE '%{query}%'"
    results = db.session.execute(query)
    products = [dict(p) for p in results]
    return render_template('searchresults.html', query=query)


@app.route('/generate_qr/<int:pid>/<int:price>')
def generate_qr_route(pid,price):
    img = generate_qr(price)
    img.save('qr.png')
    
    return send_file('qr.png', mimetype='image/png')



if __name__ == "__main__":
    app.config['UPLOAD_FOLDER'] = 'static/images/'
    app.run(debug = True,port = 5005)
