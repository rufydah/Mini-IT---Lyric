from flask import Flask, render_template,request, redirect,url_for, session #render_template is load HTML file  from templates folder 
from flask_sqlalchemy import SQLAlchemy 
app = Flask(__name__) 
app.secret_key = 'mook_user_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_db.db' #Database configuration
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #disable deprecated modification tracking warning
db = SQLAlchemy(app)
class User(db.Model):#Define user model
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80),unique=True, nullable=False)#Username cannot be empty
    password = db.Column(db.String(120),nullable=False) #password cannot be empty
@app.route('/')
def index():
    return "<h2>User System</h2> <a href='/user/register'>Register</a> | <a href='/user/login'>Login</a>"
@app.route('/user/register', methods=['GET','POST'])
def user_register():
    if request.method == 'POST':#Check if this is a POST request
        uname = request.form['username']
        pwd = request.form['password']
        new_user = User(username=uname,password=pwd)
        db.session.add(new_user) #Add record to database session
        db.session.commit()
        return redirect('/user/login') #After register success,redirect to login page
    return render_template('register.html') #Get request: show register html page
@app.route('/user/login', methods=['GET','POST'])
def user_login():
    if request.method == 'POST':
        uname = request.form['username']#Get username input
        pwd = request.form['password']
        user = User.query.filter_by(username=uname,password=pwd).first()#Search user with matching username and password
        if user:
            session['user_logged_in'] = True #Mark user as logged in
            return "Login success! You can go to the playlist page."
        else:
            return "Wrong username or password"
    return render_template('login.html') #Get request:show login html page
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True,host="0.0.0.0",port=5001)   #host is accessible by other devices on smae wifi     
      

    