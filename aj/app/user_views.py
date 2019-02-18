import os
import random
import re
import uuid

from flask import Blueprint, render_template, jsonify, \
    session, request, url_for, g
from werkzeug.utils import redirect

from app.models import User
from utils.function import login_required

user_blue = Blueprint('user', __name__)


@user_blue.route('/register/', methods=['GET'])
def register():
    return render_template('register.html')


@user_blue.route('/register/', methods=['POST'])
def my_register():
    # 获取参数
    mobile = request.form.get('mobile')
    imagecode = request.form.get('imagecode')
    passwd = request.form.get('passwd')
    passwd2 = request.form.get('passwd2')
    # 1. 验证参数是否都填写了
    if not all([mobile, imagecode, passwd, passwd2]):
        return jsonify({'code': 1001, 'msg': '请填写完整的参数'})
    # 2. 验证手机号正确
    if not re.match('^1[3456789]\d{9}$', mobile):
       return jsonify({'code': 1002, 'msg': '手机号不正确'})
    # 3. 验证图片验证码
    if session['img_code'] != imagecode:
        return jsonify({'code': 1003, 'msg': '验证码不正确'})
    # 4. 密码和确认密码是否一致
    if passwd != passwd2:
        return jsonify({'code': 1004, 'msg': '密码不一致'})
    # 验证手机号是否被注册
    user = User.query.filter_by(phone=mobile).first()
    if user:
        return jsonify({'code': 1005, 'msg': '手机号已被注册，请重新注册'})
    # 创建注册信息
    user = User()
    user.phone = mobile
    user.name = mobile
    user.password = passwd
    user.add_update()
    return jsonify({'code': 200, 'msg': '请求成功'})


@user_blue.route('/code/', methods=['GET'])
def get_code():
    # 获取验证码
    # 方式1: 后端生成图片，并返回验证码图片的地址（不推荐）
    # 方式2: 后端只生成随机参数，返回给页面，在页面中在生成图片（前端做）
    s='1234567890qwertyuioplkjhgfdsazxcvbnmQWERTYUIOPLKJHGFDSAZXCVBNM'
    code = ''
    for i in range(4):
        code += random.choice(s)
    session['img_code'] = code
    return jsonify({'code': 200, 'msg': '请求成功', 'data': code})


@user_blue.route('/login/', methods=['GET'])
def login():
    return render_template('login.html')


@user_blue.route('/my_login/', methods=['GET'])
def my_login():
    # 实现登录
    phone = request.args.get('phone')
    pwd = request.args.get('pwd')
    # 1. 校验参数是否填写完成
    if not all([phone, pwd]):
        return jsonify({'code':1006, 'msg':'请将请求参数填写完整'})
    # 2. 获取手机号对应的用户信息
    user = User.query.filter(User.phone == phone).first()
    if not user:
        return jsonify({'code':1007, 'msg': '该账号没有注册，请去注册'})
    # 3. 校验密码是否正确
    if not user.check_pwd(pwd):
        return jsonify({'code': 1008, 'msg': '密码不正确'})
    # 4. 登录标识设置
    session['user_id'] = user.id
    return jsonify({'code': 200, 'msg': '请求成功'})


@user_blue.route('/my/', methods=['GET'])
@login_required
def my():
    return render_template('my.html')


@user_blue.route('/user_info/', methods=['GET'])
@login_required
def user_info():
    # 获取用户基本信息
    user_id = session['user_id']
    user = User.query.get(user_id)
    return jsonify({'code':200, 'msg': '请求成功', 'data': user.to_basic_dict()})


@user_blue.route('/profile/', methods=['GET'])
def profile():
    return render_template('profile.html')


@user_blue.route('/my_profile/', methods=['POST'])
def my_profilte():
    if request.method == 'GET':
        id = g.id
        user = User.query.get(id)
        print(user)
        name = user.name
        phone = user.phone
        avatar = user.avatar
        return render_template(my.html, name=name, phone=phone, avatar=avatar)
    if request.method == 'POST':
        id = g.id
        # 修改用户名
        if request.form.get('name'):
            user = User.query.get(id)
            user.name = request.form.get('name')
            user.add_update()
            return redirect(url_for('house.y'))


@user_blue.route('/auth/', methods=['GET'])
def auth():
    return render_template('auth.html')

@user_blue.route('/auth/', methods=['POST'])
def my_auth():
    name = User.query.get('id_name')
    card = User.query.get('id_cart')
    # 验证名字
    if not all(name, card):
        return jsonify({'code':200, 'msg':'请求成功'})
    else:
        return jsonify({'code':1008, 'msg':'请输入合法名字'})

    # 验证身份证号码





