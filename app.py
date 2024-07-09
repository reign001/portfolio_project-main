from __future__ import annotations
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TelField, FileField, TextAreaField
from wtforms.validators import DataRequired
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Integer, String, ForeignKey, LargeBinary
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import smtplib


 





app = Flask(__name__)
app.secret_key = "Enebo"
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = b'd577dd402dc52d93bb4c0267992023913ae77c81da696dd3c6513187c7b9ee93'

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///ARTIFARE.db"
db.init_app(app)

class User(UserMixin, Base):
    __tablename__ = "User"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    First_Name: Mapped[str] = mapped_column(String(20), nullable=False)
    Last_Name: Mapped[str] = mapped_column(String(20), nullable=False)
    Phone_Number: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    Email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    Street: Mapped[str] = mapped_column(String(20), nullable=False)
    City: Mapped[str] = mapped_column(String(20), nullable=False)
    State: Mapped[str] = mapped_column(String(20), nullable=False)
    Country: Mapped[str] = mapped_column(String(20), nullable=False)
    Password: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.today)
    children = relationship("Item", back_populates="user")
    
    
class Item(Base):
    __tablename__ = "Item"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_image:  Mapped[LargeBinary] = mapped_column(LargeBinary, nullable=False)
    item_name: Mapped[str] = mapped_column(String(50), nullable=False)
    item_description: Mapped[str] = mapped_column(String(300), nullable=False)
    item_price: Mapped[int] = mapped_column(Integer, nullable=False)
    inserted_at: Mapped[datetime] = mapped_column(default=datetime.today)
    user_id: Mapped[int] = mapped_column(ForeignKey('User.id'))
    parent = relationship("user", back_populates="children")
    children = relationship("Order", back_populates="item")
    

    
class Order(Base):
    __tablename__ = "Order"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_name: Mapped[str] = mapped_column(String(50), nullable=False)
    order_price: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id: Mapped[int] = mapped_column(ForeignKey('Item.id'))
    parent = relationship("Item", backref="children")
    
    
# with app.app_context():
#     db.create_all()
    #   db.session.add(new_user)
    #   db.session.commit()

class SignUp_Form(FlaskForm):
    """this is a form for the signup page"""
    First = StringField('First Name', validators=[DataRequired()])
    Last = StringField('Last Name', validators=[DataRequired()])
    Phone = TelField(label='Phone Number', validators=[DataRequired()])
    Email = EmailField(label='email', validators=[DataRequired()])
    Street = StringField(label='street', validators=[DataRequired()])
    City = StringField(label='city', validators=[DataRequired()])
    State = StringField(label='state', validators=[DataRequired()])
    Country = StringField(label='country', validators=[DataRequired()])
    Password = PasswordField('Password', [DataRequired()])
  
    
    
#class Login_Form(FlaskForm):
#     """this is a form for the login page"""
#     email = EmailField(label='email')
#     password = PasswordField(label='password')


 
class Market_Form(FlaskForm):
    """this is a form for the signup page"""
    image_name = StringField(label='Give your image a name', validators=[DataRequired()])
    image_type = StringField('Describe your image type') 
    image_description = TextAreaField('Describe your image', validators=[DataRequired()])
    upload_image = FileField( validators=[DataRequired()])

# Create a user_loader callback
@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)





@app.route("/")
def home():
    # form2 = Login_Form()
    return render_template("landing.html")

@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    form = SignUp_Form()
    if request.method == "POST":
        with app.app_context():
            new_user = User(
                First_Name = request.form.get("First"),
                Last_Name = request.form.get("Last"),
                Phone_Number = request.form.get("Phone"),
                Email = request.form.get("Email"),
                Street = request.form.get("Street"),
                City = request.form.get("City"),
                State = request.form.get("State"),
                Country = request.form.get("Country"),
                Password = request.form.get("Password"))
            try:
                db.session.add(new_user)
                db.session.commit()
            except:    
                print("unsuccessful")
        return redirect(url_for('sign_up'))
    return render_template("sign_up.html", form = form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        email = request.form.get("email_form")
        password = request.form.get("password_form")
        
        # Find user by email entered.
        with app.app_context():
            result = db.session.execute(db.select(User).where(User.Email == email))
            user = result.scalar()
        
          # Check stored password hash against entered password hashed.
        if user.Password == password:
            login_user(user)
            return redirect(url_for('welcome'))
    
    return render_template('login.html')    
    

@app.route("/welcome", methods=["POST", "GET"])
def welcome():
    return render_template('welcome.html')

@app.route('/market', methods=["POST", "GET"])
def market():
    market_form = Market_Form()
    market_form.validate_on_submit()
    return render_template('market.html', form=market_form)



@app.route('/nature', methods=["POST", "GET"])
def nature():
    year_time = datetime.now().year
    return render_template("nature.html")

@app.route('/pencil', methods=["POST", "GET"])
def pencil():
    year_time = datetime.now().year
    return render_template("pencil.html")


@app.route('/paint', methods=["POST", "GET"])
def paint():
    year_time = datetime.now().year
    return render_template("paint.html")
@app.route("/gallery", methods=["POST", "GET"])
def gallery():
    return render_template("gallery.html")





if __name__=="__main__":
    app.run(debug=1)