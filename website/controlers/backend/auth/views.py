from flask import render_template, redirect, request, url_for
from flask_login import login_user, logout_user, login_required, \
    current_user
from website.blueprints import backend
from website.helper.email import send_email
from website.models.user import User
from werkzeug.security import generate_password_hash


@backend.before_app_request
def before_request():
    if current_user.is_authenticated:
        print(current_user.confirmed)
        if not current_user.confirmed:
                # and request.endpoint \
                # and request.endpoint[:8] != 'backend.' \
                # and request.endpoint != 'static':
            return redirect(url_for('backend.unconfirmed'))


@backend.route('/auth/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('backend.index'))
    return render_template('backend/auth/unconfirmed.html')


@backend.route('/auth/login', methods=['GET', 'POST'])
def login():
    """登录"""
    if (request.method == 'POST'):  # 提交表单
        email = request.form.get('email')
        user = User.get(User.email == email)
        if user and user.verify_password(request.form.get('password')):  # 验证密码
            login_user(user)
            return redirect(url_for('backend.index'))
        return '邮箱或密码有错.'

    # return render_template('backend/auth/login.html')
    return render_template('backend/template_new.html')


@backend.route('/auth/logout')
@login_required
def logout():
    """退出登录"""
    logout_user()
    return '你已退出登录.'


@backend.route('/auth/register', methods=['GET', 'POST'])
def register():
    """用户注册"""
    if (request.method == 'POST'):  # 提交表单
        # 写入数据库
        email = request.form.get('email')
        username = request.form.get('username')
        password_hash = generate_password_hash(request.form.get('password'))
        user = User(email=email, username=username, password_hash=password_hash)
        user.save()
        # 发送邮箱验证
        token = user.generate_confirmation_token()
        send_email(user.email, '邮箱验证',
                   'backend/auth/email/confirm', user=user, token=token)

        return '注册成功,已发送邮件!'

    return render_template('backend/auth/register.html')


@backend.route('/auth/confirm/<token>')
@login_required
def confirm(token):
    """验证邮箱"""
    if current_user.confirmed:  # 已验证过
        return redirect(url_for('backend.index'))
    if current_user.confirm(token):  # 验证通过
        return '验证成功!'
    else:
        return '该链接已失效.'
    return redirect(url_for('backend.index'))


@backend.route('/auth/confirm')
@login_required
def resend_confirmation():
    """重新发送邮箱验证"""
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, '邮箱验证',
               'backend/auth/email/confirm', user=current_user, token=token)
    return '邮件已重新发送'


@backend.route('/auth/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """修改密码"""
    if (request.method == 'POST'):  # 提交表单
        if current_user.verify_password(request.form.get('old_password')):  # 验证密码输入是否正确
            current_user.password_hash = generate_password_hash(request.form.get('new_password'))
            current_user.save()  # 保存密码
            return '密码修改成功'

    return render_template("backend/auth/change_password.html")


@backend.route('/auth/reset', methods=['GET', 'POST'])
def password_reset_request():
    """重置密码之发送邮件"""
    if not current_user.is_anonymous:
        return redirect(url_for('backend.index'))

    if (request.method == 'POST'):  # 提交表单
        email = request.form.get('email')
        user = User.get(User.email == email)
        if user:
            token = user.generate_reset_token()
            send_email(user.email, '重置密码',
                       'backend/auth/email/reset_password',
                       user=user, token=token)
            return '重置密码的邮件已发送'

    return render_template('backend/auth/reset_password_email.html')


@backend.route('/auth/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    """重置密码"""
    if not current_user.is_anonymous:
        return redirect(url_for('backend.index'))
    if (request.method == 'POST'):  # 提交表单
        email = request.form.get('email')
        user = User.get(User.email == email)
        if user is None:
            return '用户不存在.'
        if user.reset_password(token, request.form.get('password')):
            return '重置密码成功.'
        return '操作失败.'

    return render_template('backend/auth/reset_password.html')
