# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask , render_template, request, redirect

#flask-sqlalchemy -it is a orm mapper it help us to do changes in database with the help of python
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
app.app_context().push()

class Todo(db.Model):
    srno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"{self.srno} - {self.title}"

# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/', methods = ['GET', 'POST'])
# ‘/’ URL is bound with home() function.
def home():
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title = title, desc = desc)
        db.session.add(todo)
        db.session.commit()

    allTodo = Todo.query.all()
    return render_template("index.html", allTodo = allTodo)


@app.route('/about')
# ‘/about URL is bound with about() function.
def about():

    return render_template("aboutTodo.html")

@app.route('/delete/<int:srno>')
# ‘/delete URL is bound with delete() function.
def delete(srno):

    todo = Todo.query.filter_by(srno = srno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route('/update/<int:srno>', methods = ['GET', 'POST'])
# ‘/update URL is bound with update() function.
def update(srno):
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(srno = srno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')

    todo = Todo.query.filter_by(srno = srno).first()
    return render_template("updateTodo.html", todo = todo)

# main driver function
if __name__ == '__main__':

	# run() method of Flask class runs the application 
	# on the local development server.
	app.run(debug=True, port=5000)
