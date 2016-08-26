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
import webapp2
import cgi
import re

page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>SignUp</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>
        <a href="/">Sign Up</a>
    </h1>
"""

page_footer = """
</body>
</html>
"""


info = """
 <form action="/" method="post">
<label for="username">Username</label>
    <input type="text" value='{4}' name="username">
    <label class=error>{0}</label><br/>
    <label for="password">Password</label>
    <input type="password" name="password" value=""/>
    <label class=error>{1}</label><br/>
    <label for="repass">Confirm Password</label>
    <input type="password" name="repass" value=""/>
    <label class=error>{2}</label><br/>
    <label for="email">E-mail Address</label>
    <input type="text"  value='{5}' name="email">
    <label class=error>{3}</label><br/>
    <input type="submit" value ="Submit"/>
  </form>"""

class Index(webapp2.RequestHandler):
    def get(self):
        response = page_header + info.format("","","","","","") + page_footer
        self.response.write(response)

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        repass = self.request.get("repass")
        email = self.request.get("email")
        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        PASS_RE = re.compile("^.{3,20}$")
        EMAIL_RE = re.compile("^[\S]+@[\S]+.[\S]+$")
        user_error = ""
        pass_error = ""
        verify_error = ""
        email_error = ""
        error = False

        if not USER_RE.match(username):
            user_error = "Invalid Username"
            error = True
        if not PASS_RE.match(password):
            pass_error = "Invalid Password"
            error = True
        if not repass == password:
            verify_error = "Your passwords do not match"
            error = True
        if email:
            if not EMAIL_RE.match(email):
                email_error = "Invalid E-mail"
                error = True
        if error == True:
            response = page_header + info.format(user_error, pass_error, verify_error, email_error, username, email) + page_footer
            self.response.write(response)
        else:
            self.redirect('/Welcome?username={}'.format(username))

class WelcomePage(webapp2.RequestHandler):
    def get(self):

        username = self.request.get("username")

        response = page_header + "<p>" + "Welcome, " + username + "!" + "<p/>" + page_footer
        self.response.write(response)

app = webapp2.WSGIApplication([
    ('/', Index),
    ('/Welcome', WelcomePage)
], debug=True)
