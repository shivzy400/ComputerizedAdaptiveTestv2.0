from AdaptiveTest import app , db , bcrypt
from flask import redirect , render_template , url_for , flash  , request , abort
from AdaptiveTest.models import User , Result , Question
from AdaptiveTest.forms import LoginForm , RegistrationForm , UpdateAccountForm , QuestionForm , TestForm
from flask_login import login_user , current_user , logout_user , login_required
from random import randint

@app.route('/')
@app.route('/homepage')
def home_page() :
    return render_template('home.html' , title = 'Home')

@app.route('/register' , methods=['GET' , 'POST'])
def register_page() :
    if current_user.is_authenticated :
        return redirect(url_for('home_page'))
    form = RegistrationForm()
    if form.validate_on_submit() :
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            name = form.name.data ,
            username = form.username.data , 
            gender = form.gender.data ,
            password = hashed_password
        )
        db.session.add(user)
        db.session.commit()

        flash('Registered Successfully' , 'success')
        return redirect(url_for('home_page'))
    return render_template('register.html' , title = 'Register' , form = form)

@app.route('/login' , methods=['GET' , 'POST'])
def login_page() :
    if current_user.is_authenticated :
        return redirect(url_for('home_page'))
    form = LoginForm()
    if form.validate_on_submit() :
        user = User.query.filter_by(username =form.username.data).first()
        if user and bcrypt.check_password_hash(user.password , form.password.data) :
            login_user(user , remember = form.remember.data)
            next_page = request.args.get('next')
            flash(f'Logged in Successfully.' , 'success')
            return redirect(next_page) if next_page else redirect(url_for('home_page'))
        else :
            flash(f'Incorrect Username or Password.' , 'danger')
 
    return render_template('login.html' , title = 'Login' , form = form)

@app.route('/logout')
def logout() :
    logout_user()
    return redirect(url_for('home_page'))

@app.route('/feeds')
def feeds_page() :
    return render_template('feeds.html' , title = 'Feeds')

@app.route('/rules')
def rules_page() :
    return render_template('rules.html' , title = 'Rules')

@app.route('/account/<string:username>')
def account(username) :
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('account.html' , title = 'Account' , user = user)

@app.route('/update_account' , methods=['GET' , 'POST'])
@login_required
def update_account() : 

    form = UpdateAccountForm()
    if form.validate_on_submit() :
        print('fine')
        current_user.username = form.username.data
        current_user.name = form.name.data
        current_user.gender = form.gender.data
        db.session.commit()
        flash(f'Account Updated.' , 'success')
        return redirect(url_for('home_page'))
    
    elif request.method == 'GET' :
        form.username.data = current_user.username
        form.name.data = current_user.name
        form.gender.data = current_user.gender

    return render_template('update_account.html' , title = 'Edit Account' , form = form)

@app.route('/pre_test')
@login_required
def pretest_page() :
    return render_template('pretest_screen.html' , user = current_user , title = 'Ready?')

@app.route('/test' , methods = ['GET' , 'POST'])
@login_required
def test_page() :
    count = 0
    form = TestForm()
    form.options.process_data(0)
    questions = list(Question.query.all())
    idx = randint(0,len(questions)-1)
    if not count :
        return render_template('test_page.html' , title = 'Test' , count = idx + 1 ,  question = questions[idx] , form = form)

@app.route('/admin_login')
def admin_login() :
    form = LoginForm()
    form.options.default = 0
    form.process()
    return render_template('admin_login.html')