from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True # setting for 2 things-learning about ORM and how flask apps/apps connect to dbs, and useful for debugging issues when the app isn't talking to your db like you expect it to
db = SQLAlchemy(app) #calling a sqlalchemy constructor, pass in flask application to bind together. this creates a db object we can now use
app.secret_key = 'dbljh408h0ejOHSEOghaev0EY'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, date, owner):
        self.title = title
        self.body = body
        self.date = date
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'blog', 'index'] # these are named after their FUNCTIONS
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['email'] = email
            flash("Logged in")
            print(session)
            return redirect('/blog_form')
        else:
            flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html', title="Log in to your blog!")

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    email_err = ''
    pw_err = ''
    verify_err = ''

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

        if email != '':
            if '@' not in email or '.' not in email:
                email_err = "Invalid email."

        if password == '' or password == " " or len(password) < 3 or len(password) > 20 or ' ' in password:
            pw_err = "Invalid password - must be between 3-20 characters in length and contain no spaces."

        if verify != password:
            verify_err = "Passwords must match."

        existing_user = User.query.filter_by(email=email).first() #if user doesn't exist, variable will = None

        if existing_user:
            flash('User already exists', 'error')

        if not existing_user and not email_err and not pw_err and not verify_err:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            return redirect('/blog_form')

    return render_template('signup.html', title="Sign up for a Blog!", email_err=email_err, pw_err=pw_err, verify_err=verify_err)

@app.route('/')
def index():
    users = User.query.all()

    return render_template('index.html', title="All Blog Users", users=users)

@app.route('/blog')
def blog_list():

    owner = User.query.filter_by(email=session['email']).first()

    if request.args.get("id"):
        blog_id = request.args.get('id')
        blog = Blog.query.get(blog_id)
        blog_date = request.args.get('date')
        return render_template("single_post.html", blog=blog, blog_date=blog_date)

    elif request.args.get("user"):
        user_id = request.args.get('user')
        user = User.query.get(user_id)
        posts = Blog.query.filter_by(owner=user).order_by(Blog.date.desc()).all()
        return render_template("single_user.html", user=user, posts=posts)

    else:
        #posts = Blog.query.all()
        #posts = Blog.query.filter_by(owner=owner).all()
        posts = Blog.query.order_by(Blog.date.desc()).all()
        return render_template('blog_list.html', title="Build-a-blog!", posts=posts, owner=owner)

@app.route('/blog_form', methods=['GET', 'POST'])
def new_post():

    if request.method == 'GET':
        return render_template("blog_form.html", title="Add New Blog Post")

    if request.method == 'POST':
        title = request.form['blog-title']
        body = request.form['blog-body']
        date = request.args.get('date')
        owner = User.query.filter_by(email=session['email']).first()
        title_error = ""
        body_error = ""

        if len(title) < 1:
            title_error = "Please enter a title."

        if len(body) < 1:
            body_error = "Please fill in a blog post."

        if not title_error and not body_error:
            new_blog = Blog(title, body, date, owner)
            db.session.add(new_blog)
            db.session.commit()
            #blog_id = new_blog.id
            # return redirect('/single_post?id={0}'.format(blog_id))
            blog_url = "/blog?id=" + str(new_blog.id)
            return redirect(blog_url)

        return render_template("blog_form.html", title="Add New Blog Post", title_error=title_error, body_error=body_error)

@app.route('/logout')
def logout():
    del session['email']
    flash('Logged out')
    return redirect('/blog')

if __name__ == '__main__':
    app.run()
