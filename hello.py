import email
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = EmailField('What is your UofT Email address?',
                       [DataRequired(), Email()])
    submit = SubmitField('Submit')


app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)

app.config['SECRET_KEY'] = 'kjsdfkasdjfklsdnflasdclaskdfsjaldfms'


@app.route("/", methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        email: str = session.get('email')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        if email is not None and 'utoronto' not in email:
            print("here")
            session["email_msg"] = 'Please use your UofT email address'
        elif email is not None and 'utoronto' in email:
            session['email_msg'] = "Your UofT Email is " + email
        else:
            session['email_msg'] = ''
        session['name'] = form.name.data
        session['email'] = form.email.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), email_msg=session.get('email_msg'))


@app.route("/user/<name>")
def user(name):
    return render_template("user.html", name=name, current_time=datetime.datetime.utcnow())
