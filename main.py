import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session
from passlib.hash import pbkdf2_sha256
from model import Donation, Donor, User

app = Flask(__name__)
app.secret_key = "1234a" #os.environ.get('SECRET_KEY').encode()


@app.route('/')
def home():
    return redirect(url_for('all'))


@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)


@app.route('/login/', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        user = User.select().where(User.name == request.form['name']).get()
        if user and pbkdf2_sha256.verify(request.form['password'], user.password):
            session['username'] = request.form['name']
            return redirect(url_for('create'))
        else:
            return render_template('login.jinja2', error="Incorrect user name")
    else:
        return render_template('login.jinja2')


@app.route('/create/', methods=["GET", 'POST'])
def create():
    if 'username' not in session:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            list = Donor.select().where(Donor.name.contains(request.form['name']))
            if len(list)==0:
                donor = Donor(name=request.form['name'])
                donor.save()
            else:
                donor = Donor.select().where(Donor.name==request.form['name']).get()
            donation = Donation(value=request.form['donation'], donor=donor)
            donation.save()
            return redirect(url_for('all'))

        else:
            return render_template('create.jinja2')




if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

