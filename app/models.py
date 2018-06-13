from app.extensions import db, login_manager
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,current_user
from .forms import EmailGoForm
from datetime import datetime

class User(UserMixin, db.Model):



    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True)
    confirmed = db.Column(db.Boolean, default=False)
    icon = db.Column(db.String(40), default='default.jpg')




    #这样的方法可以通过对象来调用
    @property
    def password(self):
        raise AttributeError('不能访问密码属性')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 密码校验
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 生成用于账户激活的token
    def generate_activate_token(self, expires_in=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'id': self.id})


     #生成用于邮箱密码的验证
    def generate_activated_token(self,new_email, expires_in=3600):
        # self.email = new_email
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'id': self.id,'email':new_email })

    # 校验账户激活的token
    @staticmethod
    def check_activate_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        u = User.query.get(data['id'])
        if not u:
            return False
        # 用户没有激活
            # u.email = token['email']
        if not u.confirmed:
            u.confirmed = True
            db.session.add(u)
        return True
    #校验邮箱更改的
    @staticmethod
    def check_activated_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        u = User.query.get(data['id'])
        if not u:
            return False
        # 用户没有激活
        else:
            u.email = data['email']
            db.session.add(u)
            return True

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rid = db.Column(db.Integer, index=True, default=0)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    # 添加外键
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))

#电影字段
class Move(db.Model):
    postid = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(128))
    content_title = db.Column(db.Text)
    duration = db.Column(db.Integer,index = True)
    publish_time = db.Column(db.DateTime, default=datetime.utcnow)
    like_num = db.Column(db.Integer,index = True)
    share_num = db.Column(db.Integer,index = True)
    icon = db.Column(db.String(168), default='default.jpg')

# 回调函数
@login_manager.user_loader
def load_user(uid):
    return User.query.get(uid)














