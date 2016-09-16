
#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#rename test from powershell
#renamed and committing
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Formation</title>
</head>
<body>
    <h1>Sign Up</h1>
"""

page_footer = """
</body>
</html>
"""

edit_header_txt = "<h2>Signup</h2>"

#TODO: Fix HTML (replace username for all other fields. Watch Substituting into our form - Udacity,
#will help with understanding variable substituting placing variables from Python into html
#%(error_username) is a variable
form = """
<form name="form" method="post" action="/">
    <label for="username">Username</label><input name="username" value="%(username)s">
<div style="color: red">%(error_username)s</div>
        <br>
    <label for="password">Password</label><input type="password" name="password">
<div style="color: red">%(error_password)s</div>
        <br>
    <label for="verify">Password Verify</label><input type="password" name="verify">
<div style="color: red">%(error_verify)s</div>
        <br>
    <label for="email">Email (Optional)</label><input name="email" value="%(email)s">
<div style="color: red">%(error_email)s</div>
        <br>
    <input type="submit" value="Submit"/>
</form>
"""

import re
import webapp2
import cgi

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)
#below are variables to pass into the form (to populate the form).  Dictionary used
class Signup(webapp2.RequestHandler):
    def write_form(self, error_username="", error_password="", error_verify="", error_email="", username="", email=""):
        self.response.out.write(form % {
                                        "username": username,
                                        "email": email,
                                        "error_username": error_username,
                                        "error_password": error_password,
                                        "error_verify": error_verify,
                                        "error_email": error_email
                                        })
#get form from server , form HTML is returned to client
    def get(self):
        #TODO:get rid of render and replace with appropriate function  write_form  used to make the view
        #do the same for all renders
        #self.render("signup-form.html")
        #self.response.out.write(form)

        self.write_form()
#Where is verify defined*********************?????????????????????????
#Post answer (user input??) here back to server. Then redirect back to client
    def post(self):
        have_error = False
        user_username = self.request.get('username')
        user_password = self.request.get('password')
        user_verify = self.request.get('verify')
        user_email = self.request.get('email')
#different variables used below to test validity of user input

        username = valid_username(user_username)
        password = valid_password(user_password)
        #added line below
        verify = user_password == user_verify
        email = valid_email(user_email)

        params = dict(username = user_username, email = user_email)


        if not username:
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not password:
            params['error_password'] = "That wasn't a valid password."
            have_error = True

        if not verify:
    #elif password != user_verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True


        if not email:
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
#            self.render('signup-form.html', **params)
            self.write_form(**params)
        else:
#       next line:  good code
            self.redirect('/Welcome?username=' + user_username)

#       next line:  "good code"
            # self.response.out.write("Thanks!")
            # self.redirect('/Welcome?username={}'.format(user_username))
#        self.response.out.write("username")
#            print "username"


class Welcome(webapp2.RequestHandler):
#TEsting...comment next 4 lines of code


    def get(self):
        username = self.request.get("username")
        self.response.out.write("Welcome {}.".format(username))
#        self.response.out.write("Welcome"+ username)
app = webapp2.WSGIApplication([('/', Signup),
                               ('/Welcome', Welcome)],
                              debug=True)
