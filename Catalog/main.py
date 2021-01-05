from flask import Blueprint,render_template, url_for, request, flash,redirect
from flask_login import login_required, current_user
from .models import Workout,User
from . import db

main = Blueprint('main',__name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html',name=current_user.name, email=current_user.email)

@main.route('/new')
def new_workout():
    return render_template('create_workout.html')


@main.route('/new',methods=['POST'])
@login_required
def new_workout_post():
    pushups = request.form.get('pushups') 
    comment = request.form.get('comment')  
    workout = Workout(pushups=pushups,comment=comment,author=current_user)
    db.session.add(workout)
    db.session.commit()
    flash('Your workout has been added.')
    return redirect(url_for('main.user_workouts'))


@main.route('/all',methods=['GET'])
@login_required
def user_workouts():
    user = User.query.filter_by(email=current_user.email).first_or_404()
    workouts = user.workouts
    return render_template('all.html',user=user,workouts=workouts)
    

@main.route('/workouts/<int:workout_id>/update',methods=['GET','POST'])
@login_required
def update_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    if request.method=='POST':
        workout.pushups = request.form['pushups']
        workout.comment = request.form['comment']
        db.session.commit()
        flash('The workout has been updated.')
        return redirect(url_for('main.user_workouts'))
    else:
        return render_template('update_workout.html',workout=workout)


@main.route('/workouts/<int:workout_id>/delete',methods=['GET'])
@login_required
def delete_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    db.session.delete(workout)
    db.session.commit()
    return redirect(url_for('main.user_workouts'))
