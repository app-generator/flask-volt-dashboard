from flask import render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_user,
    logout_user
)

from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm
from apps.authentication.models import Users

from apps.authentication.util import verify_pass

from translate import Translator
from apps.translate.models import Reviews
from datetime import datetime
#from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

import os

#def translate_text(sl, tl, t2t, model_path):

#  model = M2M100ForConditionalGeneration.from_pretrained(model_path)
#  tokenizer = M2M100Tokenizer.from_pretrained(model_path)

  # translate Hindi to French
#  tokenizer.src_lang = sl
#  encoded_sl = tokenizer(t2t, return_tensors="pt")
#  generated_tokens = model.generate(**encoded_sl, forced_bos_token_id=tokenizer.get_lang_id(tl))
  
#  return tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)

@blueprint.route('/translate', methods=['GET', 'POST'])
@blueprint.route('/index', methods=['GET', 'POST'])
@blueprint.route('/', methods=['GET', 'POST'])
def route_default():

  if request.method == 'GET':
    return render_template('home/translate.html')

  else:

    # read the posted values from the UI
    _sl = request.form['slang']
    _tl = request.form['tlang']
    _t2t = request.form['t2t']
    _tt = request.form['tt']

    lcode = {"1" : ['es', 'Ndyuka (Aukaans)'], "2" : ['en', 'English'], "3" : ['fr', 'French']}
    msg = 'Translation successful'
    translation = ''
    
    if _sl == '':
      msg = 'Select the source language'
    elif _tl == '':
      msg = 'Select the target language'
    elif _t2t == '':
      msg = 'Provide the text to translate'
    elif _sl == _tl:
      msg = 'Please select different source and target languages'
    #elif (_sl == '2' or _sl == '3') and (_tl == '2' or _tl == '3'):
    #  msg = 'You can only translate to/from Ndyuka (Aukaans)'

    if 'translate' in request.form:
      if msg == 'Translation successful':
        #model_path = 'apps/models/m2m100_djk_en_bigger_no_bible_es'
        #translation = translate_text(lcode.get(_sl)[0], lcode.get(_tl)[0], _t2t, model_path)
        translation = Translator(to_lang = lcode.get(_tl)[0], from_lang = lcode.get(_sl)[0]).translate(_t2t)
        _tt = translation
      else:
        _tt = ''

      return render_template('home/translate.html',
        t2t = _t2t,
        sl = _sl,
        tl = _tl,
        msg = msg,
        translation = _tt)

    elif 'review' in request.form:

      _comment = request.form['revcomment']
      _revText = request.form['revText']

      if msg == 'Translation successful':
        if _revText == _tt:
          msg = 'Please review translation before saving'
        else:
          record = Reviews(lcode.get(_sl)[1], lcode.get(_tl)[1], _t2t, _tt, _revText, _comment, datetime.now())
          db.session.add(record)
          db.session.commit()

          msg = 'Review successful'

      else:
        msg = 'Generate a translation first'

      return render_template('home/translate.html',
        t2t = _t2t,
        sl = _sl,
        tl = _tl,
        msg = msg,
        translation = _tt)

    elif 'accept' in request.form:

      _comment = request.form['acceptcomment']

      if msg == 'Translation successful':
        translation = Translator(to_lang = lcode.get(_tl)[0], from_lang = lcode.get(_sl)[0]).translate(_t2t)

        record = Reviews(lcode.get(_sl)[1], lcode.get(_tl)[1], _t2t, translation, _tt, _comment, datetime.now())
        db.session.add(record)
        db.session.commit()

        msg = 'Translation saved'

      else:
        msg = 'Generate a translation first'

      return render_template('home/translate.html',
        t2t = _t2t,
        sl = _sl,
        tl = _tl,
        msg = msg,
        translation = _tt)


# Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = Users.query.filter_by(username=username).first()

        # Check the password
        if user and verify_pass(password, user.password):

            login_user(user)
            return redirect(url_for('authentication_blueprint.route_default'))

        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Wrong user or password',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/register_new_user_admin', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']

        # Check usename exists
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Username already registered',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        user = Users(**request.form)
        db.session.add(user)
        db.session.commit()

        return render_template('accounts/register.html',
                               msg='User created please <a href="/login">login</a>',
                               success=True,
                               form=create_account_form)

    else:
        return render_template('accounts/register.html', form=create_account_form)


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login'))


# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500
