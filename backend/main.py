from flask import flash, redirect, render_template, request, send_file, session, url_for, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from itsdangerous import SignatureExpired
from models import User, NFT, photo_processing
from forms import LoginForm, RegisterForm, UpdateAccountForm, NftForm, RequestResetForm, ResetPasswordForm
from App import app, db, login_manager, mail, serializer

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
    # token = serializer.dumps(request_data['email'], salt = 'email-confirm')
    # message = Message('Confirm Email', sender = 'ngorbunova41654@gmail.com', recipients = request_data['email'])
    # link = url_for('verification', token = token, external = True)
    # message.body = 'Your link is {}'.format(link)
    # mail.send(message)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"answer" : "done"})


# @app.route('/verification/<token>')
# def confirm_email(token):
#     request_data = request.get_json()
#     user = session.query(User).get(request_data['id'])
#     try:
#         request_data['email'] = serializer.loads(token, salt = 'email-confirm', max_age = 120)
#     except SignatureExpired:
#         return jsonify({"answer" : "verificationError"})
#     user.verification = True
#     db.session.commit()
#     return jsonify({"answer" : "done"})


@app.route('/date')
def get_current():
    users = NFT.query.all()[0]
    return jsonify(users)


@app.route("/store/id=<int:id>")
def shop(id):
    nft = NFT.query.order_by(NFT.date_creator.desc())[id]
    product = {
        "id" : nft.id,
        "name" : nft.productName,
        "image" : nft.productImage,
        "price" : nft.price,
        "authorName" : nft.authorName.username,
        "authorImage" : nft.authorName.img_name, 
        "description" : nft.description,
        "authorId" : nft.authorName_id
    }
    return jsonify(product)

    
@app.route("/store/count")
def shop_count():
    nfts = NFT.query.count()
    return jsonify({"count" : nfts})


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/settings", methods = ['POST','GET'])
def account_settings():

    form = request.form
    form_image = request.files["image"]
    author = User.query.filter_by(username = form["authorName"]).first()
    if request.method == 'POST':
        image = url_for('static', filename = 'img/' + photo_processing(form_image))
        author.general_information = form["generalInformation"]
        author.img_name = image
        db.session.commit()
        return jsonify({"answer" : "done"})
    elif request.method == 'GET':
        return jsonify(author[form["id"]])


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

    image =  url_for('static', filename = 'img/' + photo_processing(form_image))
    author = User.query.filter_by(username = form["authorName"]).first()
    new_nft = NFT(productImage = image, productName = form["name"], description = form['description'],
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
        "authorImagePath" : nft.authorName.img_name
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