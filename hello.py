import re

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, SubmitField
from wtforms.validators import DataRequired, Email

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = EmailField(
        'What is your UofT Email address?',
        validators=[DataRequired(), Email()],
    )
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')

        old_email = session.get('email')
        if old_email is not None and old_email != form.email.data:
            flash('Looks like you have changed your email!')

        session['name'] = form.name.data
        session['email'] = form.email.data

        if 'utoronto' in form.email.data.lower():
            return redirect(url_for('chat'))

        return redirect(url_for('index'))
    return render_template(
        'index.html',
        form=form,
        name=session.get('name'),
        email=session.get('email'),
    )


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    email = session.get('email', '')
    if not session.get('name') or 'utoronto' not in email.lower():
        flash('Please submit your name and a valid UofT email first.')
        return redirect(url_for('index'))

    if request.method == 'GET':
        return render_template('chat.html', name=session['name'])

    data = request.get_json(silent=True) or {}
    message = str(data.get('message', '')).strip()
    if not message:
        return {'reply': 'Please enter a message.'}, 400

    name_match = re.search(
        r'\bmy name is\s+(.+?)[.!?]*$',
        message,
        flags=re.IGNORECASE,
    )
    if name_match:
        remembered_name = name_match.group(1).strip()
        session['chat_name'] = remembered_name
        reply = f'Nice to meet you, {remembered_name}!'
    elif 'what is my name' in message.lower():
        remembered_name = session.get('chat_name')
        if remembered_name:
            reply = f'Your name is {remembered_name}.'
        else:
            reply = "You haven't told me your name yet."
    elif 'hello' in message.lower():
        reply = 'Hello!'
    else:
        reply = "I don't understand."

    return {'reply': reply}


@app.post('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)
