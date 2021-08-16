from flask import Flask,render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///posts.db"
db = SQLAlchemy(app)

class BlogPosts(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    author = db.Column(db.String(20), nullable = False, default = "N/A")
    content = db.Column(db.Text, nullable = False)
    date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return "Blog Post " + str(self.id)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/posts", methods= ["GET", "POST"])
def show_posts():

    if request.method == "POST":
        new_title = request.form["Title"]
        new_content = request.form["Content"]
        new_post = BlogPosts(title = new_title, author = "PCWiz", content= new_content)
        db.session.add(new_post)
        db.session.commit()
        return redirect("/posts")
        
    else:
        all_posts = BlogPosts.query.all()
        return render_template("posts.html", posts = all_posts)

@app.route("/posts/delete/<int:id>")
def delete(id):
    post = BlogPosts.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect("/posts")

@app.route("/posts/edit/<int:id>", methods= ["GET", "POST"])
def edit(id):
    
    post = BlogPosts.query.get_or_404(id)
    
    if request.method == "POST":
        post.title = request.form["Title"]
        post.content = request.form["Content"]
        db.session.commit()
        return redirect("/posts")

    else:
        return render_template("edit.html", post=post)


@app.route("/posts/new", methods= ["GET", "POST"])
def new_post():
    if request.method == "POST":
        post.title = request.form["Title"]
        post.content = request.form["Content"]
        new_post = BlogPosts(title = new_title, author = "PCWiz", content= new_content)
        db.session.add(new_post)
        db.session.commit()
        return redirect("/posts")

    else:
        return render_template("new_post.html")




if __name__ == "__main__":
    app.run(debug = True)