import datetime
from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, login_required, logout_user

from data import db_session
from data.users import User
from forms.user import RegisterForm, LoginForm
from sqlalchemy import or_

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'web_sh_ssd_creation'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=7)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def main():
    app.run(port=8080, host='127.0.0.1')
    db_session.global_init("db/forum.db")


@app.route('/')
def index():
    # data_dict = {'groups': [('gta 5', 0), ('gta sa', 1), ('war thunder', 2)],
    #              'categories': [(0, ('модификации', 0), ('Инфа', 1))]}
    return render_template('index.html')  # , data=data_dict)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            print(2)
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(or_(User.email == form.email.data, User.nickname == form.name.data)).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.login_or_email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        print(1)
        return redirect('/login')
    print(3)
    return render_template('register.html', title='Регистрация', form=form)


if __name__ == '__main__':
    main()
