from apps.home import blueprint
from flask import render_template, request, redirect, Response
from flask_login import login_required
from jinja2 import TemplateNotFound

from apps.translate.models import Reviews
from flask_paginate import Pagination, get_page_parameter

import io
import csv
from datetime import datetime

@blueprint.route('/dashboard', methods=['GET', 'POST'])
@blueprint.route('/dashboard.html', methods=['GET', 'POST'])
@login_required
def dashboard():

  page = request.args.get(get_page_parameter(), type=int, default=1)

  if request.method == 'POST':

    records = []
    line = ['source lang.', 'target lang.', 'text', 'translation', 'reviewed', 'comment']

    if request.form.get('allDownload'):
      records = Reviews.query.all()

      return Response(getRecords(line, records, ''), mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=reviews.csv"})

    if request.form.get('filterDownload'):

      if request.form.get('daterange'):

        _start_date, _end_date = getDateRange()

        records = filterDate(_start_date, _end_date)
        dtype = 'daterange'

        return Response(getRecords(line, records, dtype), mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=reviews.csv"})

      if request.form.get('langpair'):
        
        _slang, _tlang = getLangPair()

        records = filterLang(_slang, _tlang)
        line = ['text', 'translation', 'reviewed', 'comment']
        dtype = 'langpair'

        return Response(getRecords(line, records, dtype), mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=reviews.csv"})

      if request.form.get('langpair') and request.form.get('daterange'):

        _slang, _tlang = getLangPair()
        _start_date, _end_date = getDateRange()

        records = filterLangDate(_slang, _tlang, _start_date, _end_date)
        line = ['text', 'translation', 'reviewed', 'comment']
        dtype = 'langpair'

        return Response(getRecords(line, records, dtype), mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=reviews.csv"})

  per_page = 10
  start = 1 + (page - 1) * per_page
  end = start + per_page - 1

  reviews = Reviews.query.order_by(Reviews.reviewed_at.desc()).paginate(page, per_page, False).items
  records = Reviews.query.all()

  total = len(records)

  if end > total:
    end = total

  if start > total:
    start = total

  display_msg = 'Showing ' + str(start) + ' - ' + str(end) + ' of ' + str(total) + ' Records'

  pagination = Pagination(page=page, total=total, display_msg=display_msg, prev_label='&laquo;', next_label='&raquo;')
  
  return render_template("home/dashboard.html", reviews=reviews, pagination=pagination)

@blueprint.route('/<template>')
@login_required
def route_template(template):

  try:

    if not template.endswith('.html'):
      template += '.html'

    # Detect the current page
    segment = get_segment(request)

    # Serve the file (if exists) from app/templates/home/FILE.html
    return render_template("home/" + template, segment=segment)

  except TemplateNotFound:
    return render_template('home/page-404.html'), 404

# Helper - Extract current page name from request
def get_segment(request):

  try:

    segment = request.path.split('/')[-1]

    if segment == '':
      segment = 'index'

    return segment

  except:
    return None

def filterDate(_start_date, _end_date):

  return Reviews.query.filter(Reviews.reviewed_at.between(_start_date, _end_date))

def filterLang(_sl, _tl):
  
  return Reviews.query.filter_by(sl=_sl, tl=_tl).all()

def filterLangDate(_sl, _tl, _start_date, _end_date):
  
  return Reviews.query.filter_by(sl=_sl, tl=_tl).filter(Reviews.reviewed_at.between(_start_date, _end_date)).all()

def getLangPair():

  lcode = {"1" : ['es', 'Ndyuka (Aukaans)'], "2" : ['en', 'English'], "3" : ['fr', 'French']}
  _slang = lcode.get(request.form['slang'])[1]
  _tlang = lcode.get(request.form['tlang'])[1]

  return _slang, _tlang

def getDateRange():
  
  _start_date = datetime.strptime(request.form['startdate'], "%m/%d/%Y").strftime("%Y-%m-%d")
  _end_date = datetime.strptime(request.form['enddate'], "%m/%d/%Y").strftime("%Y-%m-%d")

  return _start_date, _end_date

def getRecords(line, records, dtype):

  output = io.StringIO()
  writer = csv.writer(output)

  writer.writerow(line)

  for row in records:
    if dtype == 'daterange' or dtype == '':
      line = [str(row.sl), str(row.tl), str(row.text), str(row.translation), str(row.reviewed), str(row.comment)]
    
    elif dtype == 'langpair':
      line = [str(row.text), str(row.translation), str(row.reviewed), str(row.comment)]
    
    writer.writerow(line)

  output.seek(0)

  return output