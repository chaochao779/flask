from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField
from wtforms.validators import Length, EqualTo, Email, DataRequired
from flask_wtf.file import FileRequired,FileAllowed,FileField
from .extensions import photos
# 用户注册表单
class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[Length(6, 20, '用户名必须在6~20个字符之间')])
    password = PasswordField('密码', validators=[Length(3, 12, '密码必须在3~12个字符之间')])
    confirm = PasswordField('确认密码', validators=[EqualTo('password', '两次密码不一致')])
    email = StringField('邮箱', validators=[Email('邮箱格式不正确')])
    submit = SubmitField('注册')


# 用户登录表单
class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired('用户名不能为空')])
    password = PasswordField('密码', validators=[DataRequired('密码不能为空')])
    remember = BooleanField('记住我')
    submit = SubmitField('登录')

#更改密码表单
class ModifyForm(FlaskForm):
    password = PasswordField('密码', validators=[DataRequired('密码不能为空')])
    new_password = PasswordField('密码', validators=[DataRequired('密码不能为空')])
    confirm_new = PasswordField('确认密码', validators=[EqualTo('new_password', '两次密码不一致')])
    submit = SubmitField('登录')
#email跳转链接表单
class EmailGoForm(FlaskForm):
    emaill = StringField('邮箱', validators=[Email('邮箱格式不正确')])
    new_email = StringField('新的邮箱', validators=[Email('邮箱格式不正确')])
    submit = SubmitField('下一步')

#上传头像的表单
class UploadForm(FlaskForm):
    photo = FileField('图像',validators=[FileRequired('请选择文件'),FileAllowed(photos, message='只能上传图片')])
    submit = SubmitField('上传')

# 发表博客表单
class PostsForm(FlaskForm):
    # 设置标签属性可以通过render_kw
    content = TextAreaField('', render_kw={'placeholder': '这一刻的想法...'},validators=[Length(3, 128, message='必须在3~128个字符之间')])
    submit = SubmitField('发表')