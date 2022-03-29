# adoption site
import os
from forms import AddForm, DelForm, AddOwnerForm
from flask import Flask, flash, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

################ SQL DATABASE ################

basedir = os.path.abspath(os.path.dirname(__file__))
database = 'data.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,database)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

################### Models ###################

class Puppy(db.Model):
    __tablename__ = 'puppies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    owner = db.relationship('Owner', backref='puppies', uselist=False)

    def __init__(self, name):
        self.name = name
        print(f'Puppy {name} created')
    
    def __repr__(self):
        if self.owner:
            return f'Puppy {self.name} with owner {self.owner.name}'
        return f'Puppy {self.name} has no owner'

class Owner(db.Model):
    __tablename__ = 'owners'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    puppy_id = db.Column(db.Integer, db.ForeignKey('puppies.id'), unique=True)

    def __init__(self, name, puppy_id):
        self.name = name
        self.puppy_id = puppy_id
        print(f'Owner {self.name} created for puppy {self.puppy_id}')
    
    def __repr__(self):
        return f'Owner name {self.name}'

################### Views ###################
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/add', methods=['GET', 'POST'])
def add_pup():
    form = AddForm()

    if form.validate_on_submit():
        name = form.name.data
        new_pup = Puppy(name)
        db.session.add(new_pup)
        db.session.commit()
        return redirect(url_for('list_pup'))
    return render_template('add.html', form=form)

@app.route('/list')
def list_pup():
    puppies = Puppy.query.all()
    return render_template('list.html', puppies=puppies)

@app.route('/delete', methods=['GET', 'POST'])
def del_pup():
    form = DelForm()

    if form.validate_on_submit():
        id = form.id.data
        pup = Puppy.query.get(id)
        db.session.delete(pup)
        db.session.commit()

        return redirect(url_for('list_pup'))
    return render_template('delete.html', form=form)

@app.route('/addowner', methods=['GET', 'POST'])
def add_owner():
    form = AddOwnerForm()

    if form.validate_on_submit():
        name = form.name.data
        puppy_id = form.puppy_id.data
        owner = Owner(name=name,puppy_id=puppy_id)
        db.session.add(owner)
        db.session.commit()
        flash({
            "name": name,
            "puppy_id": puppy_id
        })
        return redirect(url_for('add_owner'))
    return render_template('addowner.html',form=form)
    

################## Run APP ##################

if __name__ == '__main__':
    app.run(debug=True)
