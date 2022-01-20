from flask import Blueprint,redirect,url_for
from flask import render_template, request,flash
from .models import User, Note
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        global phoneNumber
        phoneNumber = request.form.get('PhoneNumber')
        password = request.form.get('Password')
        
        user = User.query.filter_by(phoneNumber=phoneNumber).first()
        if user:
            if check_password_hash(user.password, password):
                flash("You are now logged in", category="success")
                login_user(user)
                return redirect(url_for('views.bus'))#change this to the bmtc template thingy

            else:
                flash('Please check your password',category="error")
        else:
            flash('Please check your phone number, the Account doesn\'t exist',category="error")
    
    return render_template("login.html", user = current_user)

@auth.route('/logout')

def logout():
    logout_user()
    flash("You are now logged out", category="success")
    return redirect(url_for('views.home'))

@auth.route('/register',methods=['GET', 'POST'])
def register(): 
    
    
    if request.method == 'POST':
        fname = request.form.get("FirstName")
        lname = request.form.get("LastName")
        contact = request.form.get("PhoneNumber")
        password1 = request.form.get("Password")
        password2 = request.form.get("PasswordAgain")
        #print(fname,lname,contact,password1,password2)
        user = User.query.filter_by(phoneNumber=contact).first()
        if user:
            flash('Account already exists',category="error")
        elif password1 != password2:
            flash("Passwords do not match", category="error")
        elif len(password1) < 8:
            flash("Password must be at least 8 characters", category="error") 
        else:
            new_user = User(first_name=fname, last_name=lname, phoneNumber=contact, password=generate_password_hash(password1, method='sha256'))#change the method to aes in future if needed
            db.session.add(new_user)
            db.session.commit()
            
            flash("account Created", category="success")
            return redirect(url_for("views.home"))
        

    return render_template("register.html", user = current_user)
