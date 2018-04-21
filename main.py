from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:1234@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
       
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.email

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(40), unique=True) 
    body = db.Column(db.String(720))      

    def __init__(self,title,body):
        self.title = title
        self.body = body

    def __repr__(self):
        return '<User %r>' % self.title



"""@app.route('/', methods=['POST', 'GET'])
def index():

  
    blogs = Blog.query.all()
    return render_template("blog.html", blogs=blogs)"""


@app.route('/newpost', methods=["GET", "POST"])
def new_blog():

    t_error = ""
    c_error = ""

    if request.method == "GET":    
        return render_template('todos.html')
    else:
      
    
        blog = request.form['title']
        content = request.form['content']
    
        if blog.strip() == "":
            t_error = "Error! Enter valid value."
            

        if content.strip() == "":
            c_error = "Error! Enter a valid value."     
        
        if (not t_error) and (not c_error):
            blogz = Blog(blog, content)
            db.session.add(blogz)
            db.session.commit()
            return render_template("display.html", title=blog, body=content)
        else:
            return render_template("todos.html", error1=t_error, error2=c_error)



     
        
        

@app.route('/blog', methods=["GET"])
def blog():
    id = request.args.get("id")
    if not id:
        blogs = Blog.query.all()
        return render_template("blog.html", blogs=blogs)
    else:
        blog = Blog.query.get(id)
        return render_template("display.html", title=blog.title, body=blog.body)




if __name__ == '__main__':
    app.run()