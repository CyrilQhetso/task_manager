from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from app import db
from app.models import User, Task
from app.forms import RegistrationForm, LoginForm, TaskForm, UpdateTaskForm
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('main.tasks'))
    return render_template('home.html', title='Home')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.tasks'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('register.html', title='Register', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.tasks'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.tasks'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    
    return render_template('login.html', title='Login', form=form)

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@main.route('/tasks')
@login_required
def tasks():
    status_filter = request.args.get('status', 'all')
    priority_filter = request.args.get('priority', 'all')
    
    # Base query - all tasks for current user
    tasks_query = Task.query.filter_by(user_id=current_user.id)
    
    # Apply status filter
    if status_filter == 'completed':
        tasks_query = tasks_query.filter_by(completed=True)
    elif status_filter == 'pending':
        tasks_query = tasks_query.filter_by(completed=False)
    
    # Apply priority filter
    if priority_filter in ['high', 'medium', 'low']:
        tasks_query = tasks_query.filter_by(priority=priority_filter)
    
    # Order by deadline (null last) then by priority
    tasks = tasks_query.order_by(
        Task.completed.asc(),
        Task.deadline.asc().nulls_last(),
        db.case(
            (Task.priority == 'high', 1),
            (Task.priority == 'medium', 2),
            else_=3
        )
    ).all()
    
    return render_template('tasks.html', title='Tasks', tasks=tasks, 
                          status_filter=status_filter, priority_filter=priority_filter)

@main.route('/task/new', methods=['GET', 'POST'])
@login_required
def new_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            deadline=form.deadline.data,
            priority=form.priority.data,
            author=current_user
        )
        db.session.add(task)
        db.session.commit()
        flash('Your task has been created!', 'success')
        return redirect(url_for('main.tasks'))
    
    return render_template('create_task.html', title='New Task', form=form, legend='New Task')

@main.route('/task/<int:task_id>')
@login_required
def task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.author != current_user:
        abort(403)
    return render_template('task.html', title=task.title, task=task)

@main.route('/task/<int:task_id>/update', methods=['GET', 'POST'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.author != current_user:
        abort(403)
        
    form = UpdateTaskForm()
    
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.deadline = form.deadline.data
        task.priority = form.priority.data
        task.completed = form.completed.data
        db.session.commit()
        flash('Your task has been updated!', 'success')
        return redirect(url_for('main.task', task_id=task.id))
    
    elif request.method == 'GET':
        form.title.data = task.title
        form.description.data = task.description
        form.deadline.data = task.deadline
        form.priority.data = task.priority
        form.completed.data = task.completed
        
    return render_template('create_task.html', title='Update Task', 
                        form=form, legend='Update Task')

@main.route('/task/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.author != current_user:
        abort(403)
    
    db.session.delete(task)
    db.session.commit()
    flash('Your task has been deleted!', 'success')
    return redirect(url_for('main.tasks'))

@main.route('/task/<int:task_id>/toggle', methods=['POST'])
@login_required
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.author != current_user:
        abort(403)
    
    task.completed = not task.completed
    db.session.commit()
    
    return redirect(request.referrer or url_for('main.tasks'))