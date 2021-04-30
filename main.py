from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo-list.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class AddToDoForm(FlaskForm):
    todo = StringField()
    add_btn = SubmitField("Add")


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(1000), nullable=False)
    is_completed = db.Column(db.Boolean, default=False, nullable=False)



db.create_all()


@app.route('/', methods=["GET", "POST"])
def home():
    form = AddToDoForm()
    if form.validate_on_submit() and form.todo.data != "":
        new_task = Task(task=form.todo.data)
        db.session.add(new_task)
        db.session.commit()
        form.todo.data = ""
    all_tasks = db.session.query(Task).all()
    return render_template('index.html', tasks=all_tasks, form=form)


@app.route("/delete")
def delete_task():
    task_id = request.args.get('id')
    task_to_delete = Task.query.get(task_id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/done")
def check_task():
    task_id = request.args.get('id')
    task_to_check = Task.query.get(task_id)
    task_to_check.is_completed = not task_to_check.is_completed
    db.session.commit()
    return redirect(url_for('home'))




if __name__ == "__main__":
    app.run(debug=True)