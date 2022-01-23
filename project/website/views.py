from ast import Try
from flask import Blueprint,render_template
from flask import Blueprint,redirect,url_for
from flask import render_template, request,flash
from .models import User, Note
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
import os
from flask_login import login_user, login_required, logout_user, current_user
from flask_login import login_required, current_user 
import flask_login
from flask import redirect,url_for
from flask import render_template, request,flash
from .models import get_bus
import pyqrcode
import png
import qrcode
import requests
from bs4 import BeautifulSoup
from requests.sessions import dispatch_hook
from pyqrcode import QRCode
from datetime import datetime as dt
import smtplib
import random
import string,json
from cryptography.fernet import Fernet
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


views = Blueprint('views', __name__)

####defs###
def get_distance(a,b):
    # URL 
    url = f"https://www.google.com/search?&q=distace+between+{a}+bus+stop+and+{b}+bus+stop+bengaluru" 
    url = url.replace(" ", "+")
    #print(url)
    #Sending HTTP request
    req = requests.get(url)
    
    # Pulling HTTP data from internet
    sor = BeautifulSoup(req.text, "html.parser") 
    
    # Finding temperature in Celsius
    temp = sor.find("div", class_='BNeawe').text
    temp = temp.replace(")", "")  
    temp = temp.replace("(", "")  
    temp = temp.split()

    # print(temp)
    try:
        lol = temp.index("km")
    except:
        try:
            
            lol = temp.index("kms")
        except:
            lol = temp.index("minutes")
    try:
        y = lol-1
    except:
        y = "16"
    distance = temp[y]
    return distance






def chk_seats(list_obj, thing):
    number_of_seats = 0
    for i in list_obj:
        if i == thing:
            number_of_seats+=1
        else:
            pass
        if number_of_seats >= 31:###max seats in the bus
            number_of_seats = 404
    return number_of_seats



def mail(to,file,filepath):
    smtp_server = "smtp.gmail.com"
    sender_email = "bmtc.ticket@gmail.com" 
    password = "project@123"



    fromaddr = "bmtc.ticket@gmail.com" 
    toaddr = to

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = "Your Ticket has been Confirmed"

    # string to store the body of the mail
    body = "PFA Ticket"

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    filename = file
    filepath = filepath
    attachment = open(filepath, "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, password)

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    s.quit()

###enddefs###

@views.route("/", methods=['GET', 'POST'])

def home():
    
    return render_template("home.html", user= current_user)

from_loc= " "
to = "x"
from_loc_fin= " "
to_fin = "x"
list_of_busses = []
no_bus = "False"
same = "False"
phoneNumber = ""
password = ""
Bus_num = ""
email = ""

@views.route('/busses', methods=['GET', 'POST'])
@flask_login.login_required
def bus():
   
    x =1
    global from_loc
    global to
    global list_of_busses
    global no_bus
    global same
    from_loc= request.form.get('from')
    to = request.form.get('to')
    date = request.form.get('date')
    time = request.form.get('time')
    random_adr = random.randint(1000,100000000000000)
    # flash(f"{from_loc},{to},{date},{time}",category="success") #for debugging
    # flash(type(from_loc),category="success")
    if to ==None:
        pass
    else:
        list_of_busses = get_bus(from_loc,to)
        if from_loc == to:
            same = "True"
        else:
            same = "False"
        if len(list_of_busses) == 0:
            
            no_bus = "True"
        else:
            no_bus = "False"
        return redirect(url_for('views.bus_select',random_adr = random_adr))
    
    
    return render_template("busses.html", user= current_user,random_adr = random_adr)

uid = "Please_login"
user = None
@views.route('/busses/select/<random_adr>', methods=['GET', 'POST'])
@flask_login.login_required
def bus_select(random_adr):
    global phoneNumber
    global password
    global from_loc_fin
    global to_fin
    global Bus_num
    global email
    global uid
    global user
    random_adr = random.randint(1000,100000000000000)
    
    if request.method == 'POST':
        phoneNumber = request.form.get('PhoneNumber')
        password = request.form.get('Password')
        Bus_num = request.form.get('bus_number')
        Bus_num = Bus_num.upper()
        from_loc_fin= request.form.get('from')
        to_fin = request.form.get('to')
        email = request.form.get('email')

        
        user = User.query.filter_by(phoneNumber=phoneNumber).first()
        
        key = Fernet.generate_key()
        fernet = Fernet(key)
        user_1 = str(user.id)
        uid = fernet.encrypt(user_1.encode())
        if user != None:
            #flash(phoneNumber,category="success")
            if check_password_hash(user.password, password):
                return redirect(url_for('views.pay',random_adr = random_adr,uid=uid,user=user))
                #return pay(from_loc,to,phoneNumber)
            else:
                flash('Please check your password',category="error")
        else:
            pass
    return render_template("bus_select.html", user= current_user, list_of_busses=list_of_busses,samePlace=same, no_bus=no_bus,random_adr = random_adr)


track_list_seats = []
paid = "False"


@views.route('/busses/pay/<random_adr>/<uid>/<user>', methods=['GET', 'POST'])
@flask_login.login_required
def pay(random_adr,uid,user):
    global track_list_seats
    global paid
    test = get_bus(from_loc_fin,to_fin)
    random_adr = random.randint(1000,100000000000000)
    if user != None:
        try:
            if len(test) == 0:
                flash("No bus available, choose from the ones below",category="error")
                return redirect(url_for('views.bus_select',random_adr = random_adr ))
            elif to_fin not in test[Bus_num] and from_loc_fin not in test[Bus_num]:
                flash("Invalid Bus Number",category="error")
                return redirect(url_for('views.bus_select',random_adr = random_adr))
            else:
                
            
                    
                dist = get_distance(from_loc_fin, to_fin)
                number=phoneNumber
                amount = float(dist) * 1
                amount=str(amount)
                s = f"{amount} Rs is to be paid" 
                
                now = dt.now().time().strftime("%Y-%m-%d%H-%M-%S")
                peth = f"{number}{now}.png"
                cwd = os.getcwd()            ###replace this with the filepath
                dest = f"{cwd}/website/static/images/{peth}"
                
                file = peth
                
                img=qrcode.make(s)
                img.save(dest)
                track_list_seats.append(Bus_num)
                avail = chk_seats(track_list_seats,Bus_num)
                if avail == 404:
                    flash("Bus is full, choose another bus",category="error")
                    return redirect(url_for('views.bus_select',random_adr = random_adr))
                else:
                    
                    return render_template("pay.html", user= current_user,dest = dest, amount = amount,file = file, list_of_busses=list_of_busses,samePlace=same, no_bus=no_bus,paid = paid,random_adr = random_adr ) 
        except KeyError:
            
            flash("Invalid Bus Number",category="error")
            return redirect(url_for('views.bus_select',random_adr = random_adr))
    
    
@views.route('/busses/success/<random_adr>', methods=['GET', 'POST'])
@flask_login.login_required
def send_email(random_adr):
    tmp = random.randint(1000,100000000000000)
    result = ''.join((random.choice(string.ascii_lowercase) for x in range(20)))
    uid = f"{phoneNumber}{tmp}{result}{from_loc_fin}{to_fin}"
    s = f"Authorised, uid = {uid}"
    img=qrcode.make(s)
    name = uid
    cwd = os.getcwd()            ###replace this with the filepath
    destination = f"{cwd}/website/static/tickets/{name}.png"
    img.save(destination)
    
    #to commit to database, use only if rquired in future
    
    # new_Note = Note(bus_num = Bus_num,Travel_id = uid,from_loc = from_loc_fin,to=to_fin,user_id = current_user.id) 
    # db.session.add(new_Note)
    # db.session.commit()
    # flash(f"{new_Note.Travel_id},{uid}",category="success")
    id = str(current_user.id)
    user_bus_dict= {}
    list_obj = {"Bus_num":Bus_num,"uid":uid,"from_loc":from_loc_fin,"to":to_fin,"user_id":id}
    list_obj_1 = [{"Bus_num":Bus_num,"uid":uid,"from_loc":from_loc_fin,"to":to_fin,"user_id":id}]
    try:
        f = open("user_bus_dict.json")
        user_bus_dict = json.load(f)
        f.close()
        emp = user_bus_dict[id]

        emp.append(list_obj)
        dump = True
    except KeyError:
        f = open("user_bus_dict.json")
        user_bus_dict = json.load(f)
        f.close()
        user_bus_dict.update({id:list_obj_1})
        dump = True
    except json.JSONDecodeError:
        f = open("user_bus_dict.json")
        user_bus_dict={id:list_obj}
        f.close()
        dump = True
    except FileNotFoundError:
        
        user_bus_dict={id:list_obj_1}
        with open("user_bus_dict.json","w+") as out_file:

            json.dump(user_bus_dict, out_file, indent = 6)
        dump = False
    except Exception as e:
        flash("There was a problem which is yet to be rectified, I have notified the Team and they shall fix this ASAP",category="error")
        flash("Inconvinience is regretted",category="error")
        dump = False
        with open("errors.txt","w+") as f:
            f.write(str(e))
        
    if dump == True:
        with open("user_bus_dict.json","w+") as out_file:

            json.dump(user_bus_dict, out_file, indent = 6)
    
    mail(email,name,destination)
    return render_template("send_ticket.html", user= current_user,paid=paid)

@views.route('/MyBookings/', methods=['GET', 'POST'])
@flask_login.login_required
def Bookings():
    try:
        user_bus_dict = {}
        f = open("user_bus_dict.json")
        user_bus_dict = json.load(f)
        f.close()
        id = str(current_user.id)
        emp = user_bus_dict[id]

        bu=[]
        t=  []
        fro=[]
        for x in emp:
            bus = (x["Bus_num"])
            bu.append(bus)
            too = (x["to"])
            t.append(too)
            from_loc = (x["from_loc"])
            fro.append(from_loc)
        return render_template("bookings.html", user= current_user,bu=bu,t=t,fro=fro)    
    except KeyError:
        flash("You have No Bookings",category="error")
        
    except json.decoder.JSONDecodeError:
        flash("You have No Bookings",category="error")
        
    return render_template("bookings.html", user= current_user)
        
    
    
