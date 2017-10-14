from flask import Flask, request, redirect, render_template

app = Flask(__name__)
app.config['DEBUG'] = True

all_blog_entries = []

# these are request handlers below
@app.route('/', methods=['POST', 'GET'])
def index():
    
    if request.method == 'POST':
        blog_title = request.form['blog-title']
        #blog_entry = request.form['blog-enty']
        all_blog_entries.append(blog_title)

    return render_template('blog_entries.html', title="Build-a-Blog!", all_blog_entries=all_blog_entries)

app.run()