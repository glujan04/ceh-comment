# encoding: utf-8
import logging

from flask import Blueprint
from flask.views import MethodView
from ckan.common import asbool
from six import text_type

import ckan.lib.authenticator as authenticator
import ckan.lib.base as base
import ckan.lib.captcha as captcha
import ckan.lib.helpers as h
import ckan.lib.mailer as mailer
import ckan.lib.navl.dictization_functions as dictization_functions
import ckan.logic as logic
import ckan.logic.schema as schema
import ckan.model as model
import ckan.plugins as plugins
from ckan import authz
from ckan.common import _, config, g, request

log = logging.getLogger(__name__)


ceh = Blueprint(u'ceh', __name__, url_prefix=u'/ceh')

    def register(request):
      if request.POST:
         #form = UserForm(request.POST)
         if request.form.is_valid():
            cehname = request.form.get('cehname')
            cehemail = request.form.get('cehemail')
            cehcomment = request.form.get('cehcomment')

            return render(request, 'ceh_comments.html', {
                      'cehname': cehname,
                      'cehemail': cehemail,
                      'cehcomment':cehcomment, })


#ceh.add_url_rule(
#    u'/register', view_func=RegisterView.as_view(str(u'register')))

ceh.add_url_rule(u'/new', view_func=register)