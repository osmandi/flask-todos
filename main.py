from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash
import unittest
from flask_login import login_required, current_user

from app import create_app
from app.forms import LoginForm
from app.forms import TodoForm, DeleteTodoForm, UpdateTodoForm
from app.sqlite_service import get_users, get_todos, put_todos, delete_todo, update_todo


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
    username = current_user.id
    todo_form = TodoForm()
    delete_form = DeleteTodoForm()
    update_form =  UpdateTodoForm()


    #return "Hello World Platzi, tu IP es {}".format(user_ip) 
    context = {
            'user_ip': user_ip,
            'todos': get_todos(username=username),
            'username': username,
            'todo_form': todo_form,
            'delete_form': delete_form,
            'update_form': update_form
    }

    if todo_form.validate_on_submit():
            put_todos(user_id=username, description=todo_form.description.data, done=0)

            flash('Tu tarea se creo con exito!')

            return redirect(url_for('hello'))
            


     
    return render_template('hello.html', **context) # Los ** es para expandir las variables

@app.route('/todos/delete/<todo_id>', methods=['POST'])
def delete(todo_id):
        user_id = current_user.id
        print('TODO ID : {}'.format(todo_id))
        delete_todo(user_id=user_id, todo_id=todo_id)

        return redirect(url_for('hello'))

@app.route('/todos/update/<todo_id>/<int:done>', methods=['POST'])
def update(todo_id, done):
        user_id = current_user.id
        update_todo(user_id=user_id, todo_id=todo_id, done=done)

        return redirect(url_for('hello'))