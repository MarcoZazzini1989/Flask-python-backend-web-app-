from flask import Flask, render_template, request,redirect
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime




# App setup

app = Flask(__name__)
Scss(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

# Data Class
class MyTask(db.Model):
    id = db.Column( db.Integer , primary_key=True )
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Integer, default = 0)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"Task {self.id}"



# Route
# home
@app.route("/", methods=["POST","GET"])
def index():
    
    # Add task
    if request.method == "POST" :
        current_task = request.form['content']
        new_task = MyTask(content=current_task)
        try:
            db.session(new_task)
            db.commit()
            return redirect('/')
        except Exception as e:
            print(f"Error:{e}")
            return f"Error:{e}"
    # See current Task
    else:
        tasks = MyTask.query.order_by(MyTask.created).all()
        return render_template("index.html", tasks = tasks )



# Delete item
@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task = MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()  
        return redirect("/")
    except Exception as e:
        return f"Error:{e}"
    
    
# Update Task
@app.route("/update/<int:id>", methods=["GET","POST"])
def update(id):
    task = MyTask.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR:{e}")
            return "Error"
    else:
        return render_template("update.html", task=task)
    




#Runner

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()