from flask import Blueprint, render_template, flash, url_for, redirect, request,current_app
from app.forms import RegisterForm, LoginForm,ModifyForm,EmailGoForm
from app.email import send_mail
from app.models import User,Move
from app.extensions import db
from flask_login import login_user, logout_user, login_required,current_user
from app.forms import UploadForm
from app.extensions import photos
import os
from PIL import Image

user = Blueprint('user', __name__)


# 用户注册
@user.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # 根据提交的数据创建用户对象
        u = User(username=form.username.data,
                 password=form.password.data,
                 email=form.email.data)
        # 保存到数据库中
        db.session.add(u)
        # 手动提交，此时需要用到用户id
        db.session.commit()
        # 发送激活邮件
        token = u.generate_activate_token()
        send_mail('账户激活', form.email.data, 'activate.html', username=form.username.data, token=token)
        # 发送提示
        flash('注册成功，请点击邮件链接以完成激活')
        return redirect(url_for('main.index'))
    return render_template('user/register.html', form=form)


# 用户激活
@user.route('/activate/<token>/')
def activate(token):
    if User.check_activate_token(token):
        flash('激活成功')
        return redirect(url_for('user.login'))
    else:
        flash('激活失败')
        return redirect(url_for('main.index'))


@user.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # 根据用户名查找用户
        u = User.query.filter(User.username == form.username.data).first()
        if not u:
            flash('无效的用户名')
        elif not u.confirmed:
            flash('账户尚未激活，请激活后再登录')
        elif u.verify_password(form.password.data):
            # 用户登录，顺便可以完成记住我的功能
            login_user(u, remember=form.remember.data)
            flash('登录成功')
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('无效的密码')
    return render_template('user/login.html', form=form)


@user.route('/logout/')
def logout():
    # 退出登录，销毁session
    logout_user()
    flash('您已退出登录')
    return redirect(url_for('main.index'))


@user.route('/profile/')
# 路由保护
@login_required
def profile():
    return render_template('user/profile.html')


@user.route('/modiy_code/',methods=['GET', 'POST'])
@login_required
def modiy_code():
    form = ModifyForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            u = current_user._get_current_object()
            if u:
                u.password = form.new_password.data
                db.session.add(u)
                flash('您已经修改密码')
                return redirect(url_for('main.index'))
            return '没有登陆'
    return render_template('user/code.html',form = form)


@user.route('/modfiy_email/',methods=['GET', 'POST'])
@login_required
def modfiy_email():
    form = EmailGoForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            u = current_user._get_current_object()
            new_email = form.new_email.data
            token = u.generate_activated_token(new_email)
            send_mail('emmail更改', form.emaill.data, 'activateemail.html', username=u.username, token=token)
            flash('邮件发送成功，请点击邮件链接以完成激活')
            return redirect(url_for('main.index'))
            # return 'kokook'有时可以就让它跳到普通的地方，用来找哪里错误了
    return render_template('user/emaill.html',form=form)

# @user.route('/activate/<token>/')
# def activate(token):
#     User.check_activated_token(token)
#     flash('激活成功')
#     return redirect(url_for('user.login'))

@user.route('/activated/<token>/')
def activated(token):
    if User.check_activated_token(token):
        flash('email更改成功')
        return redirect(url_for('user.modfiy_email'))
    else:
        flash('email更改失败，请重新操作')
        return redirect(url_for('main.index'))

@user.route('/image/',methods = ['GET','POST'])
@login_required
def upload_image():
    form = UploadForm()
    if form.validate_on_submit():
        suffix = os.path.splitext(form.photo.data.filename)[1]
        filename = random_string() +suffix
        photos.save(form.photo.data,name = filename)
        pathname = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'],filename)
        img = Image.open(pathname)
        img.thumbnail((64, 64))

        img.save(pathname)
        if current_user.icon != 'default.jpg':
            os.remove(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], current_user.icon))
        current_user.icon = filename
        db.session.add(current_user)
    img_url = url_for('static', filename='upload/' + current_user.icon)
    return render_template('user/image.html', form=form, img_url=img_url)



@user.route('/move/',methods = ['GET','POST'])
def move():
    moves = Move.query.filter(Move.postid == 54090)
    for m in moves:

        img_urls = m.icon
    page = request.args.get('page', 1, int)
    pagination = Move.query.filter(Move.postid >=21904).paginate(page, per_page=3,error_out=False)

    Moves = pagination.items
    return render_template('user/moves.html',  pagination=pagination, Moves=Moves)
    # return render_template('user/moves.html',img_urls = img_urls,moves = moves)
@user.route('/love/',methods = ['GET','POST'])
@login_required
def love():
    page = request.args.get('page', 1, int)
    pagination = Move.query.filter(Move.postid >= 54084).paginate(page, per_page=3, error_out=False)

    Moves = pagination.items
    return render_template('user/love.html', pagination=pagination, Moves=Moves)

def random_string(length=32):
    import random
    base_dir = 'abcdefghijklmnopqrstuvwxyz1234567890'
    return ','.join(random.choice(base_dir) for i in range(length))