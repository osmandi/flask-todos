from flask import Flask, request, make_response, redirect, render_template, session
from flask_bootstrap import Bootstrap


app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'SECRETO INSEGURO'


todos = ['Comprar cafe', 'Enviar solicitud de compra', 'Entregar video al productor']

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

@app.route('/hello')
def hello():
    #user_ip = request.cookies.get('user_ip')
    user_ip = session.get('user_ip')

    #return "Hello World Platzi, tu IP es {}".format(user_ip) 
    context = {
            'user_ip': user_ip,
            'todos': todos,
            }
    return render_template('hello.html', **context) # Los ** es para expandir las variables
