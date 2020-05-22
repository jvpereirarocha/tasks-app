from flask import (
    Blueprint, render_template, request, flash, session, redirect,
    url_for, g
)
import datetime
from .extensions import db
from .models import User, Task
from .decorators import login_required
from sqlalchemy import func

bp = Blueprint('app', __name__)


@bp.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html')


@bp.route('/tasks', methods=['GET'])
@login_required
def tasks():
    current_user = session.get('user_id')
    tasks = Task.query.filter_by(user_id=current_user).all()
    description = request.args.get('description', None)
    date = request.args.get('date_task', None)
    completed = request.args.get('completed', None)
    if date is not None and date != '':
        tasks = Task.query.filter(Task.date_task.match(date)).filter_by(
            user_id=current_user).all()
        print(tasks)
    if description is not None and description != '':
        description = description.lower()
        tasks = Task.query.filter(func.lower(Task.description).contains(
            description)).filter_by(user_id=current_user).all()
    if completed is not None and completed != '' and completed != 'default':
        if completed == 'yes':
            tasks = Task.query.filter(Task.completed == True).filter_by(
                user_id=current_user).all()
            print(tasks)
        else:
            tasks = Task.query.filter(Task.completed == False).filter_by(
                user_id=current_user).all()
            print(tasks)

    return render_template('tasks/list.html', tasks=tasks)


@bp.route('/tasks/new', methods=['GET', 'POST'])
@login_required
def new_task():
    task = None
    title = 'Create Task'
    if request.method == 'POST':
        error = None
        current_user = session.get('user_id')
        description = request.form['description']
        completed = request.form['completed']
        if not description or not completed:
            error = 'Insert the description and if it\'s already completed'
        if error is None:
            check = True if completed == 'Yes' else False
            task = Task(description=description,
                        user_id=current_user, completed=check)
            db.session.add(task)
            db.session.commit()
            return redirect(url_for('app.tasks'))

        flash(error)
    return render_template('tasks/form_task.html', task=task, title=title)


@bp.route('/tasks/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_task(id):
    task = Task.query.filter_by(id=id).first()
    title = 'Edit Task'
    if request.method == 'POST':
        error = None
        current_user = session.get('user_id')
        description = request.form['description']
        completed = request.form['completed']
        if description and completed and task.user_id == current_user:
            task.description = description
            if completed == 'Yes':
                task.completed = True
            else:
                task.completed = False
            task.update_task_date = datetime.datetime.now()
            db.session.commit()
            return redirect(url_for('app.tasks'))
        else:
            error = 'Could not possible update the task'

        flash(error)

    return render_template('tasks/form_task.html', task=task, title=title)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        error = None
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        password_confirm = request.form['password_confirm']
        user = User.query.filter_by(email=email).first()
        if not first_name or not last_name or not email or not password or\
                not password_confirm:
            error = 'The credentials must be provided'
        if user:
            error = 'This email already exists'
        if password != password_confirm:
            error = 'The passwords dont\'t match'

        if error is None:
            new_user = User(first_name=first_name, last_name=last_name,
                            email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('app.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        error = None
        email = request.form['email']
        password = request.form['password']
        if not email or not password:
            error = 'The credentials must be provided'
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('app.index'))
        else:
            error = 'Invalid credentials. Check them and try again'
        flash(error)

    is_logged = session.get('user_id')
    if is_logged:
        return redirect(url_for('app.index'))

    return render_template('auth/login.html')


@bp.route('/user/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    current_user = session.get('user_id')
    user = User.query.filter_by(id=current_user).first()
    if request.method == 'POST':
        error = None
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        exists_this_email = User.query.filter_by(email=email).first()
        if not exists_this_email or user.email == email:
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            db.session.commit()
            return redirect(url_for('app.index'))
        else:
            error = 'Could not possible update the user.'
        flash(error)
    return render_template('auth/edit.html', user=user)


@bp.route('/logout', methods=['GET'])
@login_required
def logout():
    session.clear()
    return redirect(url_for('app.index'))


@bp.before_app_request
def is_logged_or_not():
    user_id = session.get('user_id')
    session['current_year'] = datetime.datetime.now().year
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).first()


@bp.after_request
def catch_response(response):
    if request.path == '/tasks':
        request.args = None
        redirect(request.path)
    return response
