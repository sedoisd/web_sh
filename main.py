import datetime
# import locale

from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data import db_session
from data.my_enum import ForumParentType, TopicParentType
from data.users import User
from data.groups import Group
from data.categories import Category, CategoryParentType
from data.forums import Forum
from data.topics import Topic
from data.posts import Post

from forms.user import RegisterForm, LoginForm
from forms.topic import TopicReplyForm, TopicCreateForm
from sqlalchemy import or_

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'web_sh_ssd_creation'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=7)


# locale.setlocale(locale.LC_TIME, 'ru_RU')

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def main():
    db_session.global_init("db/forum_v2.db")
    app.run(port=8080, host='127.0.0.1')


@app.route('/')
def index():
    session = db_session.create_session()
    groups = session.query(Group).all()
    categories_by_groups = session.query(Category).filter(Category.parent_type == CategoryParentType.group).all()
    forums_by_groups = session.query(Forum).filter(Forum.parent_type == ForumParentType.group).all()
    topics_by_groups = session.query(Topic).filter(Topic.parent_type == TopicParentType.group).all()
    return render_template('index.html', groups=groups, categories_by_groups=categories_by_groups,
                           forums_by_groups=forums_by_groups, topics_by_groups=topics_by_groups)


# view  -----------------------------------------------------------------------------
@app.route('/categories/<int:category_id>/')
def categories(category_id):
    session = db_session.create_session()
    category = session.query(Category).filter(Category.id == category_id).first()
    forums = session.query(Forum).filter(Forum.parent_type == ForumParentType.category,
                                         Forum.parent_id == category.id).all()
    return render_template('category.html', category=category, forums=forums)


@app.route('/forums/<int:forum_id>/')
def forum(forum_id):
    session = db_session.create_session()
    forum = session.query(Forum).filter(Forum.id == forum_id).first()
    topics = session.query(Topic).filter(Topic.parent_type == TopicParentType.forum,
                                         Topic.parent_id == forum.id)
    return render_template('forum.html', forum=forum, topics=topics)


@app.route('/topics/<int:topic_id>/')
def topic(topic_id):
    session = db_session.create_session()
    topic = session.query(Topic).filter(Topic.id == topic_id).first()
    posts = session.query(Post).filter(Post.topic_id == topic.id).all()
    return render_template('topic.html', topic=topic, posts=posts)


#   --------------------------------------------------------------------------------------------
# function forums  -----------------------------------------------------------------------------
@app.route('/forums/<int:forum_id>/create_topic', methods=['GET', 'POST'])  # add topic
@login_required
def create_topic(forum_id):
    form = TopicCreateForm()
    session = db_session.create_session()
    if form.validate_on_submit():
        topic = Topic(title=form.title.data, author_id=current_user.id,
                      parent_type=TopicParentType.forum, parent_id=forum_id)
        session.add(topic)
        session.commit()
        post = Post(content=form.content.data, author_id=current_user.id, topic_id=topic.id)
        session.add(post)
        session.commit()
        return redirect(f'/topics/{topic.id}/')
    return render_template('create_topic.html', form=form, forum_id=forum_id)


@app.route('/forums/<int:forum_id>/delete')  # delete forum
@login_required
def delete_forum():
    return


#   --------------------------------------------------------------------------------------------
# function topic  ------------------------------------------------------------------------------
@app.route('/topics/<int:topic_id>/reply', methods=['GET', 'POST'])  # add post in topic
@login_required
def reply_in_topic_on_the_button(topic_id):
    form = TopicReplyForm()
    session = db_session.create_session()
    topic = session.query(Topic).filter(Topic.id == topic_id).first()
    if form.validate_on_submit():
        post = Post(content=form.content.data, author_id=current_user.id, topic_id=topic_id)
        session.add(post)
        session.commit()

        topic = session.query(Topic).filter(Topic.id == topic_id).first()
        posts = session.query(Post).filter(Post.topic_id == topic.id).all()
        return render_template('topic.html', topic=topic, posts=posts)
    return render_template('reply.html', topic=topic, form=form, text_mode_title='Ответ в теме',
                           text_mode_button='Отправить')


@app.route('/topics/<int:topic_id>/delete')  # delete topic
@login_required
def delete_topic(topic_id):
    db_sess = db_session.create_session()
    topic = db_sess.query(Topic).filter(Topic.id == topic_id).first()
    if topic:
        parent_id = topic.parent_id
        help_dict = {TopicParentType.forum: 'forums', TopicParentType.group: '/',
                     TopicParentType.category: 'categories'}
        posts = db_sess.query(Post).filter(Post.topic_id == topic_id)
        db_sess.delete(topic)
        for post in posts:
            db_sess.delete(post)
        db_sess.commit()
    else:
        abort(404)
    if help_dict[topic.parent_type] == '/':
        return redirect('/')
    return redirect(f'/{help_dict[topic.parent_type]}/{parent_id}/')


#   --------------------------------------------------------------------------------------------
# function post  -------------------------------------------------------------------------------
@app.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])  # edit post
@login_required
def edit_post(post_id):
    form = TopicReplyForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        post = db_sess.query(Post).filter(Post.id == post_id, Post.author_id == current_user.id).first()
        # if current_user.id ==  :
        #     post = db_sess.query(Post).filter(Post.id == post_id).first()
        if post:
            form.content.data = post.content
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        post = db_sess.query(Post).filter(Post.id == post_id, Post.author_id == current_user.id).first()
        # if current_user.id ==:
        # post = db_sess.query(Post).filter(Post.id == post_id).first()
        if post:
            post.content = form.content.data
            post.modified_data = datetime.datetime.now()
            db_sess.commit()
            return redirect(f'/topics/{post.topic_id}/')
        else:
            abort(404)
    topic = db_sess.query(Topic).filter(Topic.id == Post.topic_id).first()
    return render_template('reply.html', title='Редактирование темы', form=form,
                           text_mode_title='Редактирование поста в теме ', text_mode_button='Изменить',
                           topic=topic)


@app.route('/posts/<int:post_id>/delete')  # delete post
@login_required
def delete_post(post_id):
    db_sess = db_session.create_session()
    post = db_sess.query(Post).filter(Post.id == post_id, Post.author_id == current_user.id).first()
    topic_id = post.topic_id
    if post:
        db_sess.delete(post)
        db_sess.commit()
    else:
        abort(404)
    return redirect(f'/topics/{topic_id}/')


#   --------------------------------------------------------------------------------------------
# authorization  -------------------------------------------------------------------------------
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
        if '@' in form.login_or_email.data:
            user = db_sess.query(User).filter(User.email == form.login_or_email.data).first()
        else:
            user = db_sess.query(User).filter(User.nickname == form.login_or_email.data).first()
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
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(or_(User.email == form.email.data, User.nickname == form.name.data)).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            nickname=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    print(form.errors)
    return render_template('register.html', title='Регистрация', form=form)


if __name__ == '__main__':
    main()
