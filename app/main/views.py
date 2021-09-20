from flask import render_template,request,redirect,url_for, abort
from flask.signals import template_rendered
from sqlalchemy.orm import load_only
from app.main import main
from .forms import UpdateProfile, PitchForm, ReviewForm
from ..models import User, Pitch, Review
from flask_login import login_required, current_user
from .. import db, photos
import datetime

#views
@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''

    title = 'Home - Welcome to Exhibit Pitch'
     # Getting reviews by category
    customer_pitches = Pitch.get_pitches('customer')
    employee_pitches = Pitch.get_pitches('employee')
    investor_pitches = Pitch.get_pitches('investor')

    return render_template('index.html', title = title, customer = customer_pitches, employee = employee_pitches, investor= investor_pitches)

@main.route('/home')
def home():
    '''
    View root page function that returns the home page and its data
    '''

    title = 'Home - Welcome to Exhibit Pitch'

    return render_template('home.html', title = title)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)


@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/pitch/new', methods = ['GET','POST'])
@login_required
def new_pitch():
    pitch_form = PitchForm()
    if pitch_form.validate_on_submit():
        title = pitch_form.title.data
        pitch = pitch_form.text.data
        category = pitch_form.category.data

        # Updated pitch instance
        new_pitch = Pitch(p_title=title,p_body=pitch,category=category,user=current_user,upvote=0,downvote=0)

        # Save pitch method
        new_pitch.save_pitch()
        return redirect(url_for('.index'))

    title = 'New pitch'
    return render_template('new_pitch.html',title = title,pitch_form=pitch_form )

@main.route('/pitch/<int:id>', methods = ['GET','POST'])
@login_required
def pitch(id):
    pitch = Pitch.get_pitch(id)
    posted_date = pitch.posted_date.strftime('%b %d, %Y')
    
    if request.args.get("upvote"):
        pitch.upvote = pitch.upvote + 1

        db.session.add(pitch)
        db.session.commit()

        return redirect("/pitch/{p_id}".format(p_id=pitch.id))

    elif request.args.get("downvote"):
        pitch.downvote = pitch.downvote + 1

        db.session.add(pitch)
        db.session.commit()

        return redirect("/pitch/{p_id}".format(p_id=pitch.id))

    review_form = ReviewForm()
    if review_form.validate_on_submit():
        review = review_form.text.data

        new_review = Review(review = review,user = current_user,p_id = pitch)

        new_review.save_review()


    reviews = Review.get_reviews(pitch)

    return render_template("pitch.html", pitch = pitch, review_form = review_form, reviews = reviews, date = posted_date)

@main.route('/investor')
@login_required
def investor():
    pitches = Pitch.get_pitches('investor')
    title= 'this investor template'
    return render_template('investors_pitches.html',title=title, pitches = pitches)

@main.route('/employee')
@login_required
def employee():
    pitches = Pitch.get_pitches('employee')
    title= 'Pitch to Employees'
    return render_template('employees_pitches.html',title=title, pitches=pitches)

@main.route('/customer')
@login_required
def customer():
    pitches = Pitch.get_pitches('customer')
    title= 'Pitch to Customers'
    return render_template('customer_pitches.html',title=title, pitches=pitches)


@main.route('/user/<uname>/pitches')
def user_pitches(uname):
    user = User.query.filter_by(username=uname).first()
    pitches = Pitch.query.filter_by(user_id = user.id).all()
    pitches_count = Pitch.count_pitches(uname)

    return render_template("profile/pitches.html", user=user,pitches=pitches,pitches_count=pitches_count)
