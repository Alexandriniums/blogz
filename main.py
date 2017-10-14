from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True # setting for 2 things-learning about ORM and how flask apps/apps connect to dbs, and useful for debugging issues when the app isn't talking to your db like you expect it to
db = SQLAlchemy(app) #calling a sqlalchemy constructor, pass in flask application to bind together. this creates a db object we can now use

#data to put in db. create a persistent class (no longer in a list)
class Blogs(db.Model):
    
    #specify datafields that should go into columns w/ this class
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))

    def __init__(self, title, body):
        self.title = title
        self.body = body

# these are request handlers below
@app.route('/', methods=['GET'])
def index():
    
    posts = Blogs.query.all()
    return render_template('blog_list.html', posts=posts)


@app.route('/newpost', methods=['GET', 'POST'])
def new_post():
    
    if request.method == 'POST':
        title = request.form['blog-title']
        body = request.form['blog-body']
        new_post = Blogs(title, body)
        db.session.add(new_post)
        db.session.commit()

    return render_template('newpost.html')

if __name__ == '__main__':
    app.run()

#@app.route("/delete-post", methods=['POST'])
#def delete_entry():
#    blog_post_id = int(request.form['blog-post-id'])
#    post = Blogs.query.get(blog_post_id)
#    db.session.delete(entry)
#    db.session.commit()
#
#    return redirect('/')