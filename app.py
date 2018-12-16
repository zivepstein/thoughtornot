from flask import Flask, render_template, request, redirect,url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField,SelectField
from wtforms.validators import DataRequired
import os
import numpy as np
from wtforms import Form, BooleanField, StringField, PasswordField, validators

def process_answer(answer, s1, s2):
	if answer == s1:
		return np.array([1,0,0])
	elif answer == s2:
		return np.array([0,1,0])
	else:
		return np.array([0,0,1])

def get_twitter_score(screen_name):
	return 0.5

class RegistrationForm(Form):
    ages = IntegerField('The ages of Mark and Adam add up to 28 years total. Mark is 20 years older than Adam. How many years old is Adam?')
    printers = IntegerField('If it takes 10 second for 10 printer to print out 10 pages of paper, how many seconds will it take 50 printers to print out 50 pages of paper?')
    bread= IntegerField('On a loaf of bread, there is a patch of mold. Every day, the patch doubles in size. If it takes 40 days for the patch to cover the entire loaf of bread, how many days would it take for the patch to cover half of the loaf of bread?')
    race= IntegerField('If you’re running a race and you pass the person in second place, what number place are you in?')
    sheeps= IntegerField('A farmer had 15 sheep and all but 8 died. How many are left?')
    hole= IntegerField('How many cubic feet of dirt are there in a hole that is 3’ deep x 3’ wide x 3’ long?')
    daughters= StringField('Emily’s father has three daughters. The first two are named April and May. What is the third daughter’s name?')
    count= SelectField('Have you seen any of the last 7 word problems before?', choices = [(0,"Yes"), (1,"No")], coerce = int)
    twitter= StringField('What is your twitter username?')


app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/', methods=['GET', 'POST'])
def hello():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        ages = process_answer(form.ages.data, 8,4)
        printers = process_answer(form.printers.data, 50,10)
        bread = process_answer(form.bread.data, 20,39)
        race = process_answer(form.race.data, 1,2)
        sheeps = process_answer(form.sheeps.data, 7,8)
        hole = process_answer(form.hole.data, 27,0)
        daughters = process_answer(form.daughters.data.lower(), "june" ,"emily")
        count = form.count.data
        screen_name = form.twitter.data
        twitter_score = get_twitter_score(screen_name)
        ncorrect =np.stack([ages, printers, bread, race, sheeps, hole, daughters]).sum(axis=0)[1]
        correct_p = float(ncorrect/7)
        return render_template('results.html', correct_p = correct_p, ncorrect = ncorrect , screen_name = screen_name, twitter_score = twitter_score)
    return render_template('index.html',form=form)


@app.route('/outro', methods=['GET', 'POST'])
def post_study():
    form = RegistrationForm(request.form)
    return render_template('index.html', form=form)

if __name__=='__main__':
    app.run()
