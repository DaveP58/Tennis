from flask import Flask, render_template,request, jsonify , redirect, url_for,flash, session
#import requests
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, label
from Model import Member, Payment, Event, session, findMember
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from wtforms.validators import DataRequired, Email, Length
from Model import getmember


app= Flask (__name__)
app.config['SECRET_KEY'] = 'TennisClubSecretKey'
engine = create_engine('sqlite:///Tennis.db', echo= False)
#Session class for database operations
Session = sessionmaker(bind=engine)
session = Session()

# Forms
class LoginForm(FlaskForm):
    recID = StringField('Rec Card ID', validators=[DataRequired(), Length(min=1, max=6)])
    submit = SubmitField('Login')
    


# Routes 
@app.route('/')
def home():
    # if username in session:
    #     return redirect(url_for('dashboard'))
    return render_template('index.html',form =LoginForm())

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        # Check if the recID exists in the database
        recID = login_form.recID.data
        user = session.query(Member).filter_by(recID=recID).first()
        if user:
             
            return render_template('dashboard.html', user=user, page='dashboard')
            
        else:
            return "User not found", 404 
    return render_template('login.html', form=login_form)

 #create a dashboard route



@app.route('/update_dashboard', methods=['POST'])
def update_dashboard():
    

    user = session.query(Member).filter_by(recID=recID).first()
    if not user:
       return redirect(url_for('login'))
 
    # Update user fields from form data
    fname = request.form.get('firstName')
    lname = request.form.get('LastName')
    phone = request.form.get('phone')
    email = request.form.get('email')
    MemberSince = request.form.get('MemberSince')
    TTExperience = request.form.get('TTExp')
    USTALevel = request.form.get('USTALevel')
    playsTennis = 'TRUE' if request.form.get('Tennis') else 'FALSE'
    playsTT = 'TRUE' if request.form.get('TableTennis') else 'FALSE'
    playsPT = 'TRUE' if request.form.get('PlatformTennis') else 'FALSE'
    playsRB = 'TRUE' if request.form.get('RedBall') else 'FALSE'
    
    session.query(Member).filter_by(recID=recID).update({
        'fname': fname,
        'lname': lname,
        'phone': phone,
        'email': email,
        'MemberSince': MemberSince,
        'TTExperience': TTExperience,
        'USTALevel': USTALevel,
        'playsTennis': playsTennis,
        'playsTT': playsTT,
        'playsPT': playsPT,
        'playsRB': playsRB
    })
    # Commit changes to the database
    session.commit()

    flash("Profile updated successfully!", "success")
    return render_template('dashboard.html', user=user, page='dashboard')

@app.route('/memdir', methods=['POST','GET'])
def memdir():
    query = request.args.get('query', '').strip()
    if query:
        members = session.query(Member.lname, Member.fname, Member.phone, Member.email,Member.playsTennis, Member.playsTT, Member.playsPT, Member.playsRB).filter(
            (Member.lname.ilike(f"%{query}%")) |
            (Member.fname.ilike(f"%{query}%")) |
            (Member.phone.ilike(f"%{query}%")) |
            (Member.email.ilike(f"%{query}%"))
        ).all()
    else:
        members = session.query(Member.lname, Member.fname, Member.phone, Member.email,Member.playsTennis, Member.playsTT, Member.playsPT, Member.playsRB).all()
    headings = ["Last Name", "First Name", "Phone", "Email", "Tennis", "TT", "PT", "Red Ball"]
    return render_template('memdir.html', members=members, headings=headings)
if __name__ == '__main__':
    app.run(debug=True)
   
