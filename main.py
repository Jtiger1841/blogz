from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:1234@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "vks9837xkj6d#$@"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship("Blog", backref='owner')
       
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(40), unique=True) 
    body = db.Column(db.String(720))  
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    

    def __init__(self,title,body,owner):
        self.title = title
        self.body = body
        self.owner = owner
    
    def __repr__(self):
        return '<User %r>' % self.title

@app.before_request
def require_login():
   allowed_routes = ['login', 'signup', 'list_blogs', 'index']
   if request.endpoint not in allowed_routes and 'username' not in session:
       return redirect('/login')



@app.route('/newpost', methods=["GET", "POST"])
def new_blog():

    t_error = ""
    c_error = ""

    if request.method == "GET":    
        return render_template('todos.html', title="Add a Blog Entry")
    else:
      
        #username = request.form['username']
        blog = request.form['title']
        content = request.form['content']
        owner = User.query.filter_by(username=session['username']).first()

        if len(blog) < 1:
            t_error = "Please enter a title"
            

        if len(content) < 1:
            c_error = "Error! Invalid Value"     
        
        if (not t_error) and (not c_error): 
            blogz = Blog(blog, content, owner)
            db.session.add(blogz)
            db.session.commit()
            return render_template("display.html", title=blog, body=content, user=owner)
        else:
            return render_template("todos.html", error1=t_error, error2=c_error)



     
        
        

@app.route('/blog', methods=["GET"])
def blog():
    if request.args.get("id"):
        blog_id = request.args.get("id")
        blog = Blog.query.get(blog_id)
        blogs =[]
        blogs.append(blog)
        return render_template("blog.html", blogs=blogs)
    elif request.args.get("user"):
        user_id = request.args.get("user")
        user = User.query.get(user_id)
        blogs = Blog.query.filter_by(owner=user).all()
        return render_template("blog.html", blogs=blogs)
    else:
        id = request.args.get("id")
        if not id:
            blogs = Blog.query.all()
            return render_template("blog.html", blogs=blogs)
        else:
            blog = Blog.query.get(id)
            return render_template("display.html", title=blog.title, body=blog.body)
        
    
    


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        U_error = ""
        pass_error = ""
        
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            db.session.add(user)
            db.session.commit()
            return redirect('/newpost')
        elif user and user.password != password:
            pass_error = "Invalid Password"
            return render_template("login.html", error2=pass_error)
        else:
            U_error = "User does not exist"
            return render_template("login.html", error1=U_error) 
    return render_template("login.html")        
        
@app.route('/signup', methods=["GET","POST"])
def signup():
    if request.method == "POST":
        U_error = ""
        pass_error = ""
        vrfy_error = ""
        user_error=""
        username = request.form['username'] 
        password = request.form['password'] 
        verify_password = request.form['verify-password'] 
        

        if username.strip() == "" or len(username) < 3 or len(username) > 25:
            U_error = "Please enter a valid username"
            username = ""

        if password.strip() == "": 
            pass_error = "Please enter a valid password"
            password = ""
        
        if password != verify_password:
            vrfy_error = "Passwords do not match"
            verify_password = ""
            password = ""  

        if (not U_error) and (not pass_error) and (not vrfy_error):
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                user_error="Error! Username Already Exist"
                return render_template("signup.html", title="Register", error1=user_error)
            else:
                new_user = User(username,password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                return redirect('/newpost')    

        else:    
            return render_template('signup.html', title="Register", error1=U_error, error2=pass_error, error3=vrfy_error )  
    return render_template("signup.html", title="Register")       
        

        
        
@app.route('/logout', methods=["GET"])
def logout():
    del session['username']
    return redirect('/blog')

@app.route('/', methods=["GET"])
def index():
    user_all = User.query.all()
    return render_template("index.html", user=user_all, title="Blogz")


if __name__ == '__main__':
    app.run()