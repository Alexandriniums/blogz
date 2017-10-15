from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True # setting for 2 things-learning about ORM and how flask apps/apps connect to dbs, and useful for debugging issues when the app isn't talking to your db like you expect it to
db = SQLAlchemy(app) #calling a sqlalchemy constructor, pass in flask application to bind together. this creates a db object we can now use

class Blogs(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/')
def index():
    
    if request.args:
        blog_id = request.args.get('id')
        blog = Blogs.query.get(blog_id)
        return render_template("blog_entry.html", blog=blog)

    else:
        posts = Blogs.query.all()
        return render_template('blog_list.html', title="Build-a-blog!", posts=posts)


@app.route('/newpost', methods=['GET', 'POST'])
def new_post():

    if request.method == 'GET':
        return render_template("newpost.html")

    if request.method == 'POST':
        title = request.form['blog-title']
        body = request.form['blog-body']
        title_error = ""
        body_error = ""

        if len(title) < 1:
            title_error = "Please enter a title."

        if len(body) < 1:
            body_error = "Please fill in a blog post."

        if not title_error and not body_error:
            new_post = Blogs(title, body)
            db.session.add(new_post)
            db.session.commit()
            #blog_id = new_post.id
            # return redirect('/blog_entry?id={0}'.format(blog_id))
            blog_url = "/?id=" + str(new_post.id)
            return redirect(blog_url)

        return render_template("newpost.html", title="Add New Blog Post", title_error=title_error, body_error=body_error)

if __name__ == '__main__':
    app.run()
