from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db= SQLAlchemy(app)

class Todo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    content=db.Column(db.String(200),nullable=False)
    completed = db.Column(db.String(20),default="[ PENDING ]",nullable=False)
    date_created = db.Column(db.String(20), default=datetime.now().strftime("%m/%d,%H:%M"))
    date_modified = db.Column(db.String(20),default=datetime.now().strftime("%m/%d,%H:%M"))

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/',methods=['POST','GET'])
def index():
    if request.method =='POST':
        task_content=request.form['contents']
        new_task=Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "there was an issue Adding your task"
        return "hello"
    else:
        tasks= Todo.query.order_by(Todo.date_created).all()
        return render_template("head.html",tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete= Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "there was a problem"


@app.route('/Pending/<int:id>')
def pending(id):
    try:
        #new_task1=task_to_delete(completed="[ PENDING ]")
        book = Todo.query.filter_by(id=id).first()
        book.completed="[ PENDING ]"
        book.date_modified=datetime.now().strftime("%m/%d,%H:%M")
        db.session.commit()
        return redirect('/')
    except:
        return "there was a problem"

@app.route('/Done/<int:id>')
def Done(id):
    try:
        book = Todo.query.filter_by(id=id).first()
        book.completed="[ DONE ]"
        book.date_modified = datetime.now().strftime("%m/%d,%H:%M")
        db.session.commit()
        return redirect('/')
    except:
        return "there was a problem"

if __name__ == '__main__':
    app.run(port='3000',debug=True)