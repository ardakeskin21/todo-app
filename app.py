from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#TODO add a end-date and delete-all or clear functionality for the todos.

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#Todo class with attributes: id, title and complete.
class Todo (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(200))
    timestamp = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    complete = db.Column(db.Boolean)
    
#returns the index page and list all the items in the Todo-list.
@app.route('/')
def index():
    todo_list = Todo.query.all()

    return render_template('index.html', todo_list = todo_list)

#method to add an item to the todo-list.
@app.route("/add", methods=["POST"])
def add_todo():
    title = request.form.get("title")
    description = request.form.get("description")
    timestamp = datetime.utcnow()
    new_todo = Todo(title=title, description=description, timestamp=timestamp, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

#method to update the state of a todo.
@app.route("/update/<int:todo_id>")
def update_todo(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))

#method to delete a todo in the list.
@app.route("/delete/<int:todo_id>")
def delete_todo(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))
    

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)