from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    done = db.Column(db.Boolean)


@app.route('/')
def index():
    #show todo
    todo_list = Todo.query.all()
    return render_template('base.html', todo_list=todo_list)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, done=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/completed/<int:todo_id>")
def completed(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.done = not todo.done
    db.session.commit()
    return redirect(url_for("index"))
    

@app.route("/update/<int:todo_id>", methods=['GET','POST'])
def update(todo_id):
    todo = Todo.query.get_or_404(todo_id)

    if request.method == "POST":
        todo.title = request.form['title']

        try:
            db.session.commit()
            return redirect(url_for("index"))
        except:
            return 'There was an issue while updating that task'

    else:
        return render_template('update.html', task=todo)


# @app.route('/update/<int:id>', methods=['GET','POST'])
# def update(id):
#     task = Todo.query.get_or_404(id)

#     if request.method == 'POST':
#         task.content = request.form['content']

#         try:
#             db.session.commit()
#             return redirect('/')
#         except:
#             return 'There was an issue while updating that task'

#     else:
#         return render_template('update.html', task=task)


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":

    db.create_all()

    app.run(debug=True)

