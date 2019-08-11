from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
import unittest

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'SECRETO INSEGURO'


todos = ['Comprar cafe', 'Enviar solicitud de compra', 'Entregar video al productor']

class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Enviar')

@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)

@app.errorhandler(500)
def internal_error(error):
    return "Error 500 {}".format(error)

@app.route('/error')
def error_server():
    return 1 / 0

@app.route('/')
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/hello'))
    #response.set_cookie('user_ip', user_ip) # Save ip user on Cookie
    session['user_ip'] = user_ip
    return response

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    #user_ip = request.cookies.get('user_ip')
    user_ip = session.get('user_ip')
    login_form = LoginForm()
    username = session.get('username')

    #return "Hello World Platzi, tu IP es {}".format(user_ip) 
    context = {
            'user_ip': user_ip,
            'todos': todos,
            'login_form': login_form,
            'username': username
            }
    # Detectara el POST
    if login_form.validate_on_submit():
        username = login_form.username.data
        # Guardar la sesion
        session['username'] = username

        flash('Nombre de usuario registrado con exito!')    

        return redirect(url_for('index'))

    return render_template('hello.html', **context) # Los ** es para expandir las variables
