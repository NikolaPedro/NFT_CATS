from turtle import done
from flask import flash, redirect, render_template, request, url_for, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from models import User, NFT
from sqlalchemy.orm import Session
import secrets
from werkzeug.security import generate_password_hash
import os
from forms import LoginForm, RegisterForm, UpdateAccountForm, NftForm, RequestResetForm, ResetPasswordForm
from App import app, db, login_manager, mail


@app.route("/")
def home():
    return render_template('index.html')


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/login", methods = ['POST'])
def json_login():
    request_data = request.get_json()
    user = User.query.filter_by(username = request_data['login']).first()
    if(user is not None):
        return jsonify({"answer" : "loginError"})
    if(user.check_password(request_data['password']) is not True):
        return jsonify({"answer" : "passwordError"})
    return jsonify({"answer" : "done"})
    # form = LoginForm()
    # print(form.validate_on_submit())

    # if current_user.is_authenticated:
    #     return redirect(url_for('shop'))

    # if form.validate_on_submit():
    #     user = User.query.filter_by(email = form.email.data).first()
    #     if user is not None and user.check_password(form.password.data):
    #         login_user(user)
    #         next = request.args.get("next")
    #         return redirect(next or url_for('shop'))
    #     flash('Invalid email address or Password.')
    # return render_template('login.html', form_login = form)


@app.route("/registration", methods = ['POST'])
def json_register():
    request_data = request.get_json()
    new_user = User(email = request_data['email'], username = request_data['login'])
    new_user.set_password(request_data['password'])
    new_user.check_password(request_data['repeatPassword'])
    if(User.query.filter_by(username = request_data['login']).first() is not None):
        return jsonify({"answer" : "loginError"})
    if(User.query.filter_by(email = request_data['email']).first() is not None):
        return jsonify({"answer" : "emailError"})
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"answer" : "done"})


@app.route('/date')
def get_current():
    users = NFT.query.all()[0]
    return jsonify(users)


@app.route("/store")
def shop():
    page = request.args.get('page', 1, type = int)
    nfts = NFT.query.all()[(page-1) * 2: page * 2]
    return jsonify(nfts)
    ##nfts = NFT.query.order_by(NFT.date_creator.desc()).paginate(page = page, per_page = 1)
    ##return render_template('store.html', nfts = nfts)


@app.route("/store/count")
def shop_count():
    nfts = NFT.query.count()
    return jsonify(nfts)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + file_ext
    picture_path = os.path.join(app.root_path, 'static/img', picture_fn)
    form_picture.save(picture_path)

    return picture_fn


@app.route("/settings", methods = ['POST','GET'])
@login_required
def account():

    request_data = request.get_json()
    if request.method == 'POST':
        if(request_data['id'] is not None):
            picture_file = save_picture(request_data['accountImage'])
            reload_user = User.query[request_data['id']](username = request_data['username'], general_information = request_data['generalInformation'], image_file = picture_file)
            db.session.commit(reload_user)
            return jsonify({"answer" : "done"})
        else:
            return redirect(url_for('json_login'))
    elif request.method == 'GET':
        return jsonify({
            "username" : reload_user.username,
            "email" : reload_user.email,
            "accountImage" : reload_user.image_file,
            "generalInformation" : reload_user.general_information
        })

    # form = UpdateAccountForm()
    # if form.validate_on_submit():
    #     if form.picture.data: 
    #         picture_file = save_picture(form.picture.data)
    #         current_user.image_file = picture_file
    #     current_user.username = form.username.data
    #     current_user.email = form.email.data
    #     current_user.general_information = form.general_information.data
    #     db.session.commit()
    #     flash('your account has been update!', 'success')
    #     return redirect(url_for('account'))
    # elif request.method == 'GET':
    #     form.username.data = current_user.username
    #     form.email.data = current_user.email
    #     form.general_information.data = current_user.general_information
    # image_file = url_for('static', filename = 'img/' + current_user.image_file )
    # return render_template('settings.html', title = 'Account', image_file = image_file, form_account = form)


@app.route("/nft/new", methods = ['POST', 'GET'])
@login_required
def new_nft():
    request_data = request.get_json()
    if (request_data['id'] is not None):
        new_nft = NFT(productImage = request_data['productImage'], productName = request_data['productName'], description = request_data['discription'],
        price = request_data['price'], authorName = request_data['id'], ownerName = request_data['id'])
        if(NFT.query.filter_by(productName = request_data['productName']).first() is not None):
            return jsonify({"answer" : "productNameError"})
        db.session.add(new_nft)
        db.session.commit()
        return jsonify({"answer":"done"})
    else:
        return redirect(url_for('json_login'))
    # form = NftForm()
    # if form.validate_on_submit():
    #     nft = NFT(image_file = form.picture.data, name = form.name.data,description = form.description.data,
    #     price = form.price.data, creator = current_user, owner = current_user)
    #     db.session.add(nft)
    #     db.session.commit()
    #     return redirect(url_for('shop'))
    # return render_template('create_nft.html', title = 'New NFT', form_nft = form)



@app.route("/store/<int:nft_id>")
@login_required
def nft(nft_id): # может быть ты json-ом будешь кидать мне id nft?
    nft = NFT.query()
    nft = NFT.query.get_or_404(nft_id)
    return jsonify({
        "productImage" : nft.productImage,
        "productName" : nft.productName,
        "description" : nft.description,
        "price" : nft.price,
        "authorName" : nft.authorName
    })
    # nft = NFT.query.get_or_404(nft_id)
    # return render_template('nft.html', title = nft.name, nft = nft)


@app.route("/user/<string:username>")
def user_accounts(username):
    user = User.query.filter_by(username = username).first_or_404()
    return render_template('profile.html', user = user)


def send_reset_email(user):
    token = user.get_reset_token()
    message = Message('Password Reset Request', sender='ngorbunova41654@gmail.com', recipients=[user.email])
    message.body = f'''To reset your password,visin the followink link:
{url_for('reset_token', token = token, _external = True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(message)


@app.route("/reset_password", methods = ['POST', 'GET'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('shop'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash('An email ha been sent with instructions to reset you password', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title = 'Reset Password', form_reset_request = form)


@app.route("/reset_password/<token>", methods = ['POST', 'GET'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('shop'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        user.past_passwrod_check(form.password.data)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('reset_token.html', title = 'Reset Password', form_reset_token = form)

if __name__ == '__main__':
    app.run(debug=True)