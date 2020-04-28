from flask import *
import re,cgi
app = Flask(__name__)
app.secret_key = "alachamtouri"

"""
this link will reset your session and then redirects you to home page
"""

@app.route("/reset",methods=['GET','POST'])
def reset():
 session.clear()
 return redirect(url_for('home'))

"""
this home page where it is required to submit your name as player in order to access the rest of the pages
"""

@app.route("/",methods=['GET','POST'])
def home():
 if request.method == 'POST':
  login = request.form.get('login')
  if login :
   session["user"]=login
   session.modified = True        
   session.permanent = True
   return redirect(url_for('easy'))
 else:
  return """
<h1>XSS GAME:</h1>
<a href="/">home</a><br><a href="/easy">easy</a><br><a href="/medium">medium</a><br><a href="/hard">hard</a><br><a href="/impossible">impossible</a><br><a href="/reset">reset</a>
<h2>Home</h2>
<br><br><form action="" method="post">
<b>Player's name:</b><input type="text" placeholder="Enter Your Name..." name="login" required>
<br><button type="submit">submit</button>
</form>"""

"""
this is easy level where any js payload will be passed without any problem
"""

@app.route("/easy",methods=['GET'])
def easy():
 if session:
  u = request.args.get('u')
  if u :
    msg="<b>Your input:</b><br><br>"+u
  else:
    msg=""
  resp = make_response( """
<h1>XSS GAME:</h1>
<a href="/">home</a><br><a href="/easy">easy</a><br><a href="/medium">medium</a><br><a href="/hard">hard</a><br><a href="/impossible">impossible</a><br><a href="/reset">reset</a>
<h2>level EASY</h2>
{}
<br><br><form action="easy" method="get">
<b>message to display:</b><input type="text" placeholder="Enter Your Message..." name="u" required>
<br><button type="submit">submit</button>
</form>""".format(msg))
  resp.set_cookie('level', "easy")
  resp.set_cookie('username', session["user"])
  return resp
 else:
    return redirect(url_for('home'))

"""
this is medium level where any js payload with "<script>" will fail, so use your imagination ;)
"""

@app.route("/medium",methods=['GET'])
def medium():
 if session:
  u = request.args.get('u')
  if u :
    if "<script>" in re.findall(r"<[^>]+>",u):
     u=cgi.escape(u,quote=True)
    msg="<b>Your input:</b><br><br>"+u
  else:
    msg=""
  resp = make_response( """
<h1>XSS GAME:</h1>
<a href="/">home</a><br><a href="/easy">easy</a><br><a href="/medium">medium</a><br><a href="/hard">hard</a><br><a href="/impossible">impossible</a><br><a href="/reset">reset</a>
<h2>level MEDIUM</h2>
{}
<br><br><form action="medium" method="get">
<b>message to display:</b><input type="text" placeholder="Enter Your Message..." name="u" required>
<br><button type="submit">submit</button>
</form>""".format(msg))
  resp.set_cookie('level', "medium")
  resp.set_cookie('username', session["user"])
  return resp
 else:
    return redirect(url_for('home'))

"""
this is hard level where you have to run js without using any js tags :p
"""

@app.route("/hard",methods=['GET'])
def hard():
 if session:
  u = request.args.get('u')
  if u :
    if  re.findall(r"<*?script.*?>",u.lower()):
     u=cgi.escape(u,quote=True)
    msg="<b>Your input:</b><br><br>"+u
  else:
    msg=""
  resp = make_response( """
<h1>XSS GAME:</h1>
<a href="/">home</a><br><a href="/easy">easy</a><br><a href="/medium">medium</a><br><a href="/hard">hard</a><br><a href="/impossible">impossible</a><br><a href="/reset">reset</a>
<h2>level HARD</h2>
{}
<br><br><form action="hard" method="get">
<b>message to display:</b><input type="text" placeholder="Enter Your Message..." name="u" required>
<br><button type="submit">submit</button>
</form>""".format(msg))
  resp.set_cookie('level', "hard")
  resp.set_cookie('username', session["user"])
  return resp
 else:
    return redirect(url_for('home'))

"""
this is level impossible where it's impossible to use any js or html payloads (it's just an example of how to fix the XSS vulnerability so don't even bother yourselves playing it xD )
"""
  
@app.route("/impossible",methods=['GET'])
def impossible():
 if session:
  u = request.args.get('u')
  if u :
    u=cgi.escape(u,quote=True)
    msg="<b>Your input:</b><br><br>"+u
  else:
    msg=""
  resp = make_response( """
<h1>XSS GAME:</h1>
<a href="/">home</a><br><a href="/easy">easy</a><br><a href="/medium">medium</a><br><a href="/hard">hard</a><br><a href="/impossible">impossible</a><br><a href="/reset">reset</a>
<h2>level IMPOSSIBLE</h2>
{}
<br><br><form action="impossible" method="get">
<b>message to display:</b><input type="text" placeholder="Enter Your Message..." name="u" required>
<br><button type="submit">submit</button>
</form>""".format(msg))
  resp.set_cookie('level', "impossible")
  resp.set_cookie('username', session["user"])
  return resp
 else:
    return redirect(url_for('home'))


app.run(host='0.0.0.0',debug=True,threaded=True,port=8888)
