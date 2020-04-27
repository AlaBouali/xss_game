from flask import *
import re,cgi
app = Flask(__name__)
app.secret_key = "secret key"

@app.route("/reset",methods=['GET','POST'])
def reset():
 session.clear()
 return redirect(url_for('home'))

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
<<br><button type="submit">submit</button>
</form>"""

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
<<br><button type="submit">submit</button>
</form>""".format(msg))
  resp.set_cookie('level', "easy")
  resp.set_cookie('username', session["user"])
  return resp
 else:
    return redirect(url_for('home'))

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
<<br><button type="submit">submit</button>
</form>""".format(msg))
  resp.set_cookie('level', "medium")
  resp.set_cookie('username', session["user"])
  return resp
 else:
    return redirect(url_for('home'))

@app.route("/hard",methods=['GET'])
def hard():
 if session:
  u = request.args.get('u')
  if u :
    if  re.findall(r"<[^>]+script[^>]+>",u.lower()):
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
<<br><button type="submit">submit</button>
</form>""".format(msg))
  resp.set_cookie('level', "hard")
  resp.set_cookie('username', session["user"])
  return resp
 else:
    return redirect(url_for('home'))
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
<<br><button type="submit">submit</button>
</form>""".format(msg))
  resp.set_cookie('level', "impossible")
  resp.set_cookie('username', session["user"])
  return resp
 else:
    return redirect(url_for('home'))


app.run(host='0.0.0.0',debug=True,threaded=True,port=8888)
