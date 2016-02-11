# -*- coding: utf-8 -*-
#
# portal/views.py: views for the portal application
# This file is part of the Manifold project.
#
# Author:
#   Mohammed Yasin Rahman <mohammed-yasin.rahman@lip6.fr>
# Copyright 2014, UPMC Sorbonne Universités / LIP6
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#   
# You should have received a copy of the GNU General Public License along with
# this program; see the file COPYING.  If not, write to the Free Software
# Foundation, 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.


"""
View Description:

Allows a user to reset their password by generating a one-time use link that can be used to reset the password, and sending that link to the user's 
registered email address.

If the email address provided does not exist in the system, this view won't send an email, but the user won't receive any error message either. 
This prevents information leaking to potential attackers. If you want to provide an error message in this case, you can subclass PasswordResetForm 
and use the password_reset_form argument.

Users flagged with an unusable password - see set_unusable_password() - aren't allowed to request a password reset to prevent misuse when using an external 
authentication source like LDAP. Note that they won't receive any error message since this would expose their account's existence but no mail will be sent either.

More Detail: https://docs.djangoproject.com/en/dev/topics/auth/default/#topics-auth-creating-users
"""

try:
    from urllib.parse import urlparse, urlunparse
except ImportError:  # Python 2
    from urlparse import urlparse, urlunparse

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, resolve_url
from django.template.response import TemplateResponse
from django.utils.http import base36_to_int
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from portal.forms import PasswordResetForm, SetPasswordForm


##
# import os.path, re
# import json
# from random                     import choice
# Avoid shadowing the login() and logout() views below.
# from django.views.generic       import View
# from unfold.loginrequired       import FreeAccessView
# from ui.topmenu                 import topmenu_items_live
# from manifold.manifoldapi       import execute_admin_query
# from manifold.core.query        import Query
# from portal.actions             import manifold_update_user
# from portal.forms               import PassResetForm
# from portal.actions             import manifold_update_user


# 4 views for password reset:
# - password_reset sends the mail
# - password_reset_done shows a success message for the above
# - password_reset_confirm checks the link the user clicked and
#   prompts for a new password
# - password_reset_complete shows a success message for the above

@csrf_protect
def password_reset(request, is_admin_site=False,
                   template_name='password_reset_form.html',
                   email_template_name='password_reset_email.html',
                   subject_template_name='registration/password_reset_subject.txt',
                   password_reset_form=PasswordResetForm,
                   token_generator=default_token_generator,
                   post_reset_redirect=None,
                   from_email=None,
                   current_app=None,
                   extra_context=None):
    if post_reset_redirect is None:
        post_reset_redirect = reverse('portal.django_passresetview.password_reset_done')
    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():

            # email check in manifold DB ###
            email = form.cleaned_data['email'].lower()  # email inserted on the form
            # @qursaan comment
            # user_query  = Query().get('local:user').select('user_id','email')
            # user_details = execute_admin_query(request, user_query)
            user_details = User.objects.all()

            flag = 0
            for user_detail in user_details:
                # @qursaan: replace '' -> .
                if user_detail.email == email:
                    flag = 1  # @qursaan: mean user have email and registered
                    break

            if flag == 0:
                messages.error(request, 'Sorry, this email is not registered.')
                return render(request, 'password_reset_form.html', {
                    'form': form,
                })
            # end of email check in manifold  ###


            opts = {
                'use_https': request.is_secure(),
                'token_generator': token_generator,
                'from_email': from_email,
                'email_template_name': email_template_name,
                'subject_template_name': subject_template_name,
                'request': request,
            }
            if is_admin_site:
                opts = dict(opts, domain_override=request.get_host())
            form.save(**opts)
            return HttpResponseRedirect(post_reset_redirect)
    else:
        form = password_reset_form()
    context = {
        'form': form,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context, current_app=current_app)


def password_reset_done(request,
                        template_name='password_reset_done.html',
                        current_app=None, extra_context=None):
    context = {}
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


# Doesn't need csrf_protect since no-one can guess the URL
@sensitive_post_parameters()
@never_cache
def password_reset_confirm(request, uidb36=None, token=None,
                           template_name='password_reset_confirm.html',
                           token_generator=default_token_generator,
                           set_password_form=SetPasswordForm,
                           post_reset_redirect=None,
                           current_app=None, extra_context=None):
    """
    View that checks the hash in a password reset link and presents a
    form for entering a new password.
    """
    UserModel = get_user_model()
    assert uidb36 is not None and token is not None  # checked by URLconf
    if post_reset_redirect is None:
        post_reset_redirect = reverse('portal.django_passresetview.password_reset_complete')
    try:
        uid_int = base36_to_int(uidb36)
        user = UserModel._default_manager.get(pk=uid_int)
    except (ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        if request.method == 'POST':
            form = set_password_form(user, request.POST)
            if form.is_valid():

                # manifold pass update ###
                # password = form.cleaned_data('password1')
                password = request.POST['new_password1']
                # user_query  = Query().get('local:user').select('user_id','email','password')
                # user_details = execute_admin_query(request, user_query)
                # @qursaan: Add this line for user table
                user_details = User.objects.all()
                # @qursaan: uncomment this for
                for user_detail in user_details:
                    if user_detail.email == user.email:  # @qursaan: change user_detail['email'] to user_detail.email
                        user_detail.password = password
                        break

                # updating password in local:user
                # @qursaan comment
                # user_params = { 'password': password}
                # manifold_update_user(request,user.email,user_params)
                # end of manifold pass update ###

                form.save()
                return HttpResponseRedirect(post_reset_redirect)
        else:
            form = set_password_form(None)
    else:
        validlink = False
        form = None
    context = {
        'form': form,
        'validlink': validlink,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


def password_reset_complete(request,
                            template_name='password_reset_complete.html',
                            current_app=None, extra_context=None):
    context = {
        'login_url': resolve_url(settings.LOGIN_URL)
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)
