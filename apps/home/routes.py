# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request, redirect, Response
from flask_login import login_required
from jinja2 import TemplateNotFound

from apps.translate.models import Reviews
from flask_paginate import Pagination, get_page_parameter

import io
import csv
from datetime import datetime

@blueprint.route('/<template>', methods=['GET', 'POST'])
@login_required
def route_template(template):

  page = request.args.get(get_page_parameter(), type=int, default=1)

  try:

    if not template.endswith('.html'):
      template += '.html'

    # Detect the current page
    segment = get_segment(request)

    if template == 'dashboard.html':

      if request.method == 'POST':

        records = []

        if request.form.get('allDownload'):
          records = Reviews.query.all()

        if request.form.get('filterDownload'):
          _start_date = request.form['startdate']
          _end_date = request.form['enddate']
          records = Reviews.query.filter(Reviews.reviewed_at.between(datetime.strptime(_start_date, '%d-%m-%Y'), datetime.strptime(_end_date, '%d-%m-%Y')))

        output = io.StringIO()
        writer = csv.writer(output)

        line = ['source lang.', 'target lang.', 'text', 'translation', 'reviewed', 'comment']
        writer.writerow(line)

        for row in records:
          line = [str(row.sl), str(row.tl), str(row.text), str(row.translation), str(row.reviewed), str(row.comment)]
          writer.writerow(line)

        output.seek(0)

        return Response(output, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=reviews.csv"})

      per_page = 10
      start = 1 + (page - 1) * per_page
      end = start + per_page - 1

      reviews = Reviews.query.order_by(Reviews.reviewed_at.desc()).paginate(page, per_page, False).items
      records = Reviews.query.all()

      total = len(records)

      if end > total:
          end = total

      display_msg = 'Showing ' + str(start) + ' - ' + str(end) + ' of ' + str(total) + ' Records'

      pagination = Pagination(page=page, total=total, display_msg=display_msg, prev_label='&laquo;', next_label='&raquo;')
      return render_template("home/" + template, segment=segment, reviews=reviews, pagination=pagination)

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
