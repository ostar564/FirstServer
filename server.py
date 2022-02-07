from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

#create flask object with file name
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db" #define connection string
db = SQLAlchemy(app)  #define database

#Create db Model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return '<Task %r>' % self.id

# route upload page to web site
@app.route('/upload')
def upload():
    return render_template('upload.html')
#route index page to root of web site
@app.route('/', methods = ['POST', 'GET'])


def index():
    if request.method == 'POST':
        #ADD TASK button clicked
        content_task = request.form['content']
        new_task = Todo(content=content_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your new task to db!!'
        
    else:
        #retrieve all data from Todo table
        tasks = Todo.query.order_by(Todo.date_created).all()
        #Send all tasks that retrieved from DB to index page
        return render_template('index.html', tasks=tasks)



#This code run when this file is call but not when it imported by other file
if __name__== "__main__":
    #start running the web page
    app.run(debug=True)