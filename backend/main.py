from flask import flash, redirect, render_template, request, send_file, url_for, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from sqlalchemy import update
from models import User, NFT, photo_processing
import secrets
from forms import LoginForm, RegisterForm, UpdateAccountForm, NftForm, RequestResetForm, ResetPasswordForm
from App import app, db, login_manager, mail

@app.route("/")
def home():
    return render_template('index.html')


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/auth", methods = ['POST'])
def json_login():
    request_data = request.get_json()
    user = User.query.filter_by(username = request_data['login']).first()
    if(user is None):
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
    nfts = NFT.query.order_by(NFT.date_creator.desc()).all()[(page-1) * 2: page * 2]
    return jsonify(nfts)
    ##nfts = NFT.query.order_by(NFT.date_creator.desc()).paginate(page = page, per_page = 1)
    ##return render_template('store.html', nfts = nfts)


@app.route("/store/image/<int:id>" , methods = ['GET'])
def store_image(id):
    request_data = request.get_json()
    nfts = NFT.query.filter_by(id = request_data["id"]).fist()
    image =  url_for('static', filename = 'img/' + nfts.productImage)
    return send_file('templates' + image, mimetype="image/jpg")


@app.route("/store/count")
def shop_count():
    nfts = NFT.query.count()
    return jsonify(nfts)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


# def save_picture(form_picture):
#     random_hex = secrets.token_hex(8)
#     _, file_ext = os.path.splitext(form_picture.filename)
#     picture_fn = random_hex + file_ext
#     picture_path = os.path.join(app.root_path, 'static/img', picture_fn)
#     form_picture.save(picture_path)

#     return picture_fn


@app.route("/settings", methods = ['POST','GET'])
@login_required
def account():

    form = request.form
    form_image = request.files["image"]
    if request.method == 'POST':
        # picture_file = save_picture(form_image['accountImage'])
        reload_user = User.query.filter_by(username = form["username"]).first()
        reload_user.imag_name = photo_processing(form_image)
        reload_user.general_information = form["description"]
        db.session.commit()
        return jsonify({"answer" : "done"})
    elif request.method == 'GET':
        return jsonify({
            "username" : reload_user.username,
            "email" : reload_user.email,
            "accountImage" : reload_user.img_name,
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


@app.route("/upload", methods = ['POST'])
def new_nft():

    if(len(list(request.files.lists())) == 0):
        return jsonify({"answer" : "imageError"})

    form = request.form
    form_image = request.files["image"]

    if(len(form["name"]) < 5):
        return jsonify({"answer" : "nameError"})

    if(float(form["price"]) < 0):
        return jsonify({"answer" : "priceError"})

    author = User.query.filter_by(username = form["authorName"]).first()
    new_nft = NFT(productImage = photo_processing(form_image), productName = form["name"], description = form['description'],
    price = form['price'], authorName = author, ownerName = author)

    db.session.add(new_nft)
    db.session.commit()
    return jsonify({"answer":"done"})

@app.route("/store/<int:nft_id>", methods = ['GET'])
def nft(nft_id): # может быть ты json-ом будешь кидать мне id nft?
    nft = NFT.query.get_or_404(nft_id)
    return jsonify({
        "imagePath" : nft.productImage,
        "name" : nft.productName,
        "description" : nft.description,
        "price" : nft.price,
        "authorName" : nft.authorName.username,
        "authorImagePath" : ""
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