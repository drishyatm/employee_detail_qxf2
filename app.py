from flask import Flask , render_template, jsonify, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Employees.sqlite3'
	
db = SQLAlchemy(app)

class Employees(db.Model):
    # Defines the Table Name employees
    __tablename__ = "employees"
    
    # Makes four columns into the table id, name, email,department
    
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(20), nullable=False)
    #department = db.relationship('Department', backref='dep_id',lazy=True)
    
    
    # A constructor function where we will pass the name and email of a employees and it gets add as a new entry in the table.
    def __init__(self, name, email, department):
        self.name = name
        self.email = email
        self.department = department
        
class Department(db.Model):        
    __tablename__ = "department"
    
    # Makes two columns into the table id,department
    
    dep_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    department = db.Column(db.String(20), nullable=False)
    
    
    # A constructor function where we will pass the department of employees and it gets add as a new entry in the table.
    def __init__(self,department):
        self.department = department
                

# Control will come here and then gets redirect to the index function
@app.route("/")
def home():
	return redirect(url_for('index'))


@app.route("/index", methods = ["GET", "POST"])
def index():
    if request.method == 'POST': 
        data = request.form # request the data from the form in index.html file
        name = data["name"]
        email = data["email"]
        department = data["department"]
        
        new_data = Employees(name, email, department)
        db.session.add(new_data)
        db.session.commit()
        
        user_data = Employees.query.all()
        
        return render_template("index.html", user_data = user_data) # passes user_data variable into the index.html file.
    
    return render_template("index.html")
	

if __name__=="__main__":
	db.create_all()
	app.run(debug=True)