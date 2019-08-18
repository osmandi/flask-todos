from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash
import unittest
from flask_login import login_required

from app import create_app
from app.forms import LoginForm
from app.sqlite_service import get_users, get_todos


app = create_app()

#todos = ['Comprar cafe', 'Enviar solicitud de compra', 'Entregar video al productor']


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
@login_required
def hello():
    #user_ip = request.cookies.get('user_ip')
    user_ip = session.get('user_ip')
    login_form = LoginForm()
    username = session.get('username')

    #return "Hello World Platzi, tu IP es {}".format(user_ip) 
    context = {
            'user_ip': user_ip,
            'todos': get_todos(username=username),
            'login_form': login_form,
            'username': username
            }
             
    '''
    users = get_users()
    for user in users:
        print(user[1])
    # Detectara el POST
    if login_form.validate_on_submit():
        username = login_form.username.data
        # Guardar la sesion
        session['username'] = username

        flash('Nombre de usuario registrado con exito!')    

        return redirect(url_for('index'))
    '''

    return render_template('hello.html', **context) # Los ** es para expandir las variables
