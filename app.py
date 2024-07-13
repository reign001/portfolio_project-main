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


#email detail for senders 
my_email = "artifare@gmail.com"
my_password = "TTghyrtf4.#"



#flask application
app = Flask(__name__)
app.secret_key = "Enebo"
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = b'd577dd402dc52d93bb4c0267992023913ae77c81da696dd3c6513187c7b9ee93'

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

#database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///ARTIFARE.db"
#database initialization
db.init_app(app)
#user table 
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
    orders = relationship("Order", back_populates="user", overlaps="orders")
    
    
class Item(Base):
    __tablename__ = "Item"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_image:  Mapped[LargeBinary] = mapped_column(LargeBinary, nullable=False)
    item_name: Mapped[str] = mapped_column(String(50), nullable=False)
    item_description: Mapped[str] = mapped_column(String(300), nullable=False)
    item_price: Mapped[int] = mapped_column(Integer, nullable=False)
    inserted_at: Mapped[datetime] = mapped_column(default=datetime.today)
    user_id: Mapped[int] = mapped_column(ForeignKey('User.id'))
    #order = relationship("Order", back_populates="items")
    

    
class Order(Base):
    __tablename__ = "Order"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_name: Mapped[str] = mapped_column(String(50), nullable=False)
    order_price: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('User.id'))
    item_id: Mapped[int] = mapped_column(ForeignKey('Item.id'))
    user = relationship("User", backref="Order")
    #items = relationship("Item", backref="order")
    
    
with app.app_context():
    db.create_all()
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
  
def convert_image_to_binary(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        item_image = file.read()
    return item_image
    
    
    

# Create a user_loader callback
@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)



@app.route("/")
def home():
    # form2 = Login_Form()
    return render_template("landing.html")

@app.route("/sign_up", methods=["GET", "POST"])
#route for user creation and database insertion
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
                print("successful")
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
        
          # Check stored password  against entered password.
        if user.Password == password:
            login_user(user)
        return redirect(url_for('welcome'))
    
    return render_template('login.html')    
    

@app.route("/welcome", methods=["POST", "GET"])
def welcome():
    return render_template('welcome.html')

#to get item detail from item table in database
@app.route("/market", methods=["GET", "POST"])
def market():
    if request.method == "POST":
        with app.app_context():
            new_item = Item(
            item_image = request.form.get("image"),
            item_name = request.form.get("name"),
            item_description = request.form.get("description"),
            item_price = request.form.get("price"))
            db.session.add(new_item)
            db.session.commit()
    return render_template("market.html")
        
    

def send_mail():
    connection = smtplib.SMTP(["smtp.gmail.com", "smtp.live.com", "smtp.mail.yahoo.com"])
    connection.starttls()
    connection.login(user=User.Email, password="password")
    connection.sendmail(from_addr=User.Email, to_addrs=my_email, msg=Item)


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
#route for gallery
@app.route("/gallery", methods=["POST", "GET"])
def gallery():
    return render_template("gallery.html")

#add to cart route
@app.route('/cart', methods=["POST", "GET"])
def cart():
    return render_template("cart.html")



if __name__=="__main__":
    app.run(debug=1)